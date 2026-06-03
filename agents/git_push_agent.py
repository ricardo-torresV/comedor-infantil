import subprocess
import sys
import os


def run(cmd: str, cwd: str | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd or os.getcwd(),
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main():
    print("=" * 55)
    print(" GIT PUSH AGENT - Subir cambios a GitHub")
    print("=" * 55)

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_dir)

    # 1. Verificar estado
    print("\n[1] Verificando estado del repositorio...")
    code, out, err = run("git status --short")
    if code != 0:
        print(f"    ERROR: {err}")
        sys.exit(1)

    if not out:
        print("    No hay cambios para subir.")
        return

    print(f"    Archivos modificados:\n{out}")

    # 2. Commit message
    msg = ""
    if len(sys.argv) > 1:
        msg = sys.argv[1]
    else:
        try:
            msg = input("[2] Mensaje del commit: ").strip()
        except EOFError:
            pass

    if not msg:
        code, out, _ = run("git log --oneline -1 --format=%s")
        last_msg = out
        msg = f"Update: {last_msg}" if last_msg else "Auto-commit from git-push-agent"
        print(f"    Usando mensaje auto-generado: {msg}")

    # 3. Add + Commit
    print("\n[3] Agregando y commitando cambios...")
    code, _, err = run("git add -A")
    if code != 0:
        print(f"    ERROR git add: {err}")
        sys.exit(1)

    code, _, err = run(f'git commit -m "{msg}"')
    if code != 0:
        if "nothing to commit" in err.lower():
            print("    No hay cambios nuevos que commitear.")
        else:
            print(f"    ERROR git commit: {err}")
            sys.exit(1)
    else:
        print("    Commit creado correctamente.")

    # 4. Push
    print("\n[4] Subiendo a GitHub...")
    code, out, err = run("git push")
    if code != 0:
        print(f"    ERROR al hacer push: {err}")
        sys.exit(1)
    print(f"    Push exitoso")

    # 5. Mostrar URL del repo
    code, out, _ = run("git remote get-url origin")
    print(f"\n    Repositorio: {out}")

    print("\n" + "=" * 55)
    print(" SUBIDA COMPLETADA")
    print("=" * 55)


if __name__ == "__main__":
    main()
