#!/usr/bin/env python3

import subprocess

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path


@dataclass(kw_only=True)
class Arguments:
    target: str
    root_cn: str | None
    client_cn: str | None
    validity: int


def parse_arguments() -> Arguments:
    parser = ArgumentParser("generate-mtls")
    parser.add_argument("--target", metavar="TARGET", type=str, help="certificate purpose, defines folder and file names (avoid whitespace)", required=True)
    parser.add_argument("--root-cn", metavar="ROOT_CN", type=str, default=None, help="root CA certificate common name")
    parser.add_argument("--client-cn", metavar="CLIENT_CN", type=str, default=None, help="client certificate common name")
    parser.add_argument("--validity", type=int, help="certificate validity in days", default=3655)
    args = parser.parse_args()

    return Arguments(**vars(args))


class CertificateGenerator:
    """Create a local self-signed root CA certificate using secp384r1 (EC) and
    signed client certificate using prime256v1 (EC)"""

    def __init__(self, args: Arguments):
        self.folder = Path(args.target)
        self.root_filename_base = self.folder / f"root@{args.target}"
        self.client_filename_base = self.folder / f"client@{args.target}"
        self.root_common_name = args.root_cn
        self.client_common_name = args.client_cn
        self.validity = args.validity

    def create_root_ca(self):
        self.folder.mkdir(exist_ok=True)
        self.create_root_key()
        self.create_root_certificate()

        print(f"Root CA:     {self.root_filename_base}.pem")

    def create_p12(self):
        self.folder.mkdir(exist_ok=True)
        self.create_client_key()
        self.create_signing_request()
        self.sign_client_certificate()
        self.create_client_p12()

        print(f"Client cert: {self.client_filename_base}.p12")

    def create_root_key(self):
        subprocess.run(
            [
                "openssl",
                "ecparam",
                "-name",
                "secp384r1",
                "-genkey",
                "-out",
                f"{self.root_filename_base}.key",
            ],
            check=True,
        )

    def create_root_certificate(self):
        subprocess.run(
            [
                "openssl",
                "req",
                "-new",
                "-key",
                f"{self.root_filename_base}.key",
                "-x509",
                "-nodes",
                "-days",
                f"{self.validity}",
                "-out",
                f"{self.root_filename_base}.pem",
                "-subj",
                f"/CN={self.root_common_name}",
                "-addext",
                "basicConstraints=critical,CA:TRUE,pathlen:0",
            ],
            check=True,
        )

    def create_client_key(self):
        subprocess.run(
            [
                "openssl",
                "ecparam",
                "-name",
                "prime256v1",
                "-genkey",
                "-out",
                f"{self.client_filename_base}.key"
            ],
            check=True,
        )

    def create_signing_request(self):
        subprocess.run(
            [
                "openssl",
                "req",
                "-new",
                "-key",
                f"{self.client_filename_base}.key",
                "-out",
                f"{self.client_filename_base}.csr",
                "-subj",
                f"/CN={self.client_common_name}",
                "-addext",
                "extendedKeyUsage = clientAuth"
            ],
            check=True,
        )

    def sign_client_certificate(self):
        subprocess.run(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                f"{self.client_filename_base}.csr",
                "-CA",
                f"{self.root_filename_base}.pem",
                "-CAkey",
                f"{self.root_filename_base}.key",
                "-CAcreateserial",
                "-out",
                f"{self.client_filename_base}.crt",
                "-days",
                f"{self.validity}",
                "-sha256",
                "-copy_extensions=copyall",
            ],
            check=True,
        )

    def create_client_p12(self):
        subprocess.run(
            [
                "openssl",
                "pkcs12",
                "-export",
                "-out",
                f"{self.client_filename_base}.p12",
                "-in",
                f"{self.client_filename_base}.crt",
                "-inkey",
                f"{self.client_filename_base}.key"
            ],
            check=True,
        )


def main() -> None:
    args = parse_arguments()
    certificate_generator = CertificateGenerator(args)
    if args.root_cn is not None:
        certificate_generator.create_root_ca()
    if args.client_cn is not None:
        certificate_generator.create_p12()


if __name__ == "__main__":
    main()
