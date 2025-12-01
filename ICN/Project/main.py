#!/usr/bin/env python3
"""
Steganographic file encryption:
- Encrypt file with AES-GCM (key from password via scrypt)
- Embed encrypted payload into PNG LSBs
- Extract and decrypt
"""

import os
import struct
from math import floor
from PIL import Image
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# === Configuration constants ===
MAGIC = b"STEGENCv1"      # 8 bytes magic/version
SALT_LEN = 16             # bytes
NONCE_LEN = 12            # AESGCM recommended nonce size
KDF_N = 2**14             # scrypt param (work factor). Tune for your machine.
KDF_R = 8
KDF_P = 1
KEY_LEN = 32              # bytes for AES-256
DEFAULT_LSB = 1           # bits per channel to use

# === Helper functions ===
def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=KEY_LEN, n=KDF_N, r=KDF_R, p=KDF_P)
    return kdf.derive(password)

def encrypt_file_to_payload(input_path: str, password: str) -> bytes:
    password_b = password.encode('utf-8')
    salt = os.urandom(SALT_LEN)
    key = derive_key(password_b, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_LEN)
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    # Payload layout: MAGIC | salt_len(1) | salt | nonce_len(1) | nonce | ciphertext_len(8) | ciphertext
    payload = bytearray()
    payload += MAGIC
    payload += struct.pack(">B", SALT_LEN)
    payload += salt
    payload += struct.pack(">B", NONCE_LEN)
    payload += nonce
    payload += struct.pack(">Q", len(ciphertext))  # 8 bytes unsigned long long
    payload += ciphertext
    return bytes(payload)

def parse_payload(payload: bytes):
    # return (salt, nonce, ciphertext)
    i = 0
    if payload[i:i+len(MAGIC)] != MAGIC:
        raise ValueError("Bad magic header")
    i += len(MAGIC)
    salt_len = payload[i]; i += 1
    salt = payload[i:i+salt_len]; i += salt_len
    nonce_len = payload[i]; i += 1
    nonce = payload[i:i+nonce_len]; i += nonce_len
    (ct_len,) = struct.unpack_from(">Q", payload, i); i += 8
    ciphertext = payload[i:i+ct_len]
    if len(ciphertext) != ct_len:
        raise ValueError("Ciphertext truncated")
    return salt, nonce, ciphertext

def decrypt_payload_to_file(payload: bytes, password: str, out_path: str):
    salt, nonce, ciphertext = parse_payload(payload)
    key = derive_key(password.encode('utf-8'), salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    with open(out_path, 'wb') as f:
        f.write(plaintext)

# === LSB embedding/extraction ===
def _bytes_to_bits(data: bytes):
    for b in data:
        for i in range(7, -1, -1):
            yield (b >> i) & 1

def _bits_to_bytes(bits):
    b = bytearray()
    cur = 0
    count = 0
    for bit in bits:
        cur = (cur << 1) | (bit & 1)
        count += 1
        if count == 8:
            b.append(cur)
            cur = 0
            count = 0
    return bytes(b)

def embed_payload_in_image(cover_image_path: str, out_image_path: str, payload: bytes, lsb: int = DEFAULT_LSB, use_alpha=False):
    img = Image.open(cover_image_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if use_alpha else "RGB")
    pixels = list(img.getdata())
    channels = 4 if img.mode == "RGBA" else 3
    channels_used = channels if (use_alpha or channels == 3) else 3
    total_bits = len(pixels) * channels_used * lsb
    if len(payload)*8 > total_bits:
        raise ValueError(f"Payload too large. Capacity bytes: {total_bits//8}, payload bytes: {len(payload)}")
    bitgen = _bytes_to_bits(payload)
    new_pixels = []
    for px in pixels:
        px_list = list(px)
        for c in range(channels_used):
            for _ in range(lsb):
                try:
                    bit = next(bitgen)
                except StopIteration:
                    bit = None
                if bit is None:
                    break
                # set LSB of px_list[c] to bit
                px_list[c] = (px_list[c] & ~1) | bit
            # continue next channel
        new_pixels.append(tuple(px_list))
    # If some pixels left unchanged (no more bits), they remain original. Good.
    stego = Image.new(img.mode, img.size)
    stego.putdata(new_pixels)
    stego.save(out_image_path, format="PNG")
    return True

def extract_payload_from_image(stego_image_path: str, lsb: int = DEFAULT_LSB, use_alpha=False) -> bytes:
    img = Image.open(stego_image_path)
    if img.mode not in ("RGB","RGBA"):
        raise ValueError("Image must be RGB or RGBA PNG")
    pixels = list(img.getdata())
    channels = 4 if img.mode == "RGBA" else 3
    channels_used = channels if (use_alpha or channels == 3) else 3
    # Reconstruct bits until we can parse header and know ciphertext length, then stop once we have full payload
    max_bits = len(pixels) * channels_used * lsb
    bits = []
    for px in pixels:
        for c in range(channels_used):
            val = px[c]
            # extract lsb bits (if lsb>1, extract that many lowest bits from MSB to LSB order)
            for b_i in range(lsb):
                bits.append((val >> (lsb-1-b_i)) & 1)  # maintain order
    # Convert bits to bytes lazily: we need at least header size to parse lengths.
    b = _bits_to_bytes(bits)
    # Now we need to parse to see full payload length. We know header minimal size:
    min_header = len(MAGIC) + 1 + SALT_LEN + 1 + NONCE_LEN + 8
    if len(b) < min_header:
        raise ValueError("Not enough data extracted for header; maybe wrong lsb or carrier.")
    # locate end of ciphertext by parsing fields from the bytes we've got; if not enough, keep extracting but we already extracted full image.
    # parse known positions similarly to parse_payload
    try:
        salt_len = b[len(MAGIC)]
        idx = len(MAGIC) + 1 + salt_len
        nonce_len = b[idx]; idx += 1
        idx += nonce_len
        (ct_len,) = struct.unpack_from(">Q", b, idx); idx += 8
    except Exception as e:
        raise ValueError("Failed to parse extracted header: " + str(e))
    needed_total = len(MAGIC) + 1 + salt_len + 1 + nonce_len + 8 + ct_len
    if len(b) < needed_total:
        raise ValueError(f"Extracted bytes incomplete. Need {needed_total} bytes, have {len(b)}. Maybe wrong image or insufficient capacity.")
    payload = b[:needed_total]
    return payload

# === Example usage ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Encrypt+Embed or Extract+Decrypt files via PNG LSB steganography")
    sub = parser.add_subparsers(dest="cmd")
    enc = sub.add_parser("embed", help="Encrypt file and embed into image")
    enc.add_argument("input_file")
    enc.add_argument("cover_image")
    enc.add_argument("out_image")
    enc.add_argument("password")
    enc.add_argument("--lsb", type=int, default=1)
    dec = sub.add_parser("extract", help="Extract payload from image and decrypt to file")
    dec.add_argument("stego_image")
    dec.add_argument("password")
    dec.add_argument("out_file")
    dec.add_argument("--lsb", type=int, default=1)
    args = parser.parse_args()

    if args.cmd == "embed":
        payload = encrypt_file_to_payload(args.input_file, args.password)
        embed_payload_in_image(args.cover_image, args.out_image, payload, lsb=args.lsb)
        print("Embedded successfully.")
    elif args.cmd == "extract":
        payload = extract_payload_from_image(args.stego_image, lsb=args.lsb)
        decrypt_payload_to_file(payload, args.password, args.out_file)
        print("Extracted and decrypted successfully.")
    else:
        parser.print_help()
