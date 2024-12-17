S_CRLF = "CRLF"
S_CR = "CR"
S_LF = "LF"
CRLF = b"\r\n"
CR = b"\r"
LF = b"\n"


def check_line_endings(file_path):
    with open(file_path, "rb") as file:
        line_endings = set()
        for line in file:
            if line.endswith(CRLF):
                line_endings.add(S_CRLF)
            elif line.endswith(LF):
                line_endings.add(S_LF)
            elif line.endswith(CR):
                line_endings.add("CR")
    return line_endings
