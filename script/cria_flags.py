import os
import sys
import random

VULN_DIR = "/home/msfadmin/vulnerable"
FLAG_FILE = "flag.txt"


_rng = random.SystemRandom()


def new_password():
    """Senha de 4 digitos (0000 a 9999)."""
    return "%04d" % _rng.randint(0, 9999)

def write_flag(password):
    if not os.path.isdir(VULN_DIR):
        os.makedirs(VULN_DIR, 0755)
    path = os.path.join(VULN_DIR, FLAG_FILE)
    f = open(path, "w")      # "w" substitui o conteudo anterior
    try:
        f.write("FLAG{%s}\n" % password)
    finally:
        f.close()
    os.chmod(path, 0644)
    return path

def normalize(text):
    """Aceita '1234' ou 'FLAG{1234}'."""
    text = text.strip()
    if text.upper().startswith("FLAG{") and text.endswith("}"):
        text = text[5:-1]
    return text

def main():
    password = new_password()
    path = write_flag(password)
    print "[+] Flag gerada em: %s" % path

    while True:
        try:
            typed = raw_input("Digite a senha de 4 digitos: ")
        except (KeyboardInterrupt, EOFError):
            print
            print "[*] Encerrado."
            break

        if normalize(typed) != password:
            print "[-] Senha incorreta. Tente novamente."
            continue

        print "[+] Senha correta!"
        try:
            answer = raw_input("Gerar uma nova flag (substitui a atual)? (s/n): ")
        except (KeyboardInterrupt, EOFError):
            print
            print "[*] Encerrado."
            break

        if answer.strip().lower() in ("s", "sim", "y", "yes"):
            password = new_password()
            path = write_flag(password)
            print "[+] Nova flag gerada em: %s" % path
        else:
            print "[*] Encerrado."
            break

if __name__ == "__main__":
    main()