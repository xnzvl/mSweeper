class Cypher:
    def __init__(
        self,
        encrypt_f: Callable[[str], str],
        decrypt_f: Callable[[str], str]
    ) -> None:
        self._encrypt_f = encrypt_f
        self._decrypt_f = decrypt_f

        self._check()

    def encrypt(
        self,
        string: str
    ) -> str:
        return self._encrypt_f(string)

    def decrypt(
        self,
        string: str
    ) -> str:
        return self._decrypt_f(string)

    def _check(
        self
    ) -> None:
        for char in ALLOWED_CHARS:
            if char != self.decrypt(self.encrypt(char)):
                raise ValueError("Invalid cypher (1:1 requested)")
