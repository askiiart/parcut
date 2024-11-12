# copied from https://github.com/blend-os/blend, and modified
class colors:
    reset = '\x1b[0m'
    bold = '\x1b[01m'
    disable = '\x1b[02m'
    underline = '\x1b[04m'
    reverse = '\x1b[07m'
    strikethrough = '\x1b[09m'
    invisible = '\x1b[08m'

    class fg:
        black = '\x1b[30m'
        red = '\x1b[31m'
        green = '\x1b[32m'
        yellow = '\x1b[33m'
        blue = '\x1b[34m'
        magenta = '\x1b[35m'
        cyan = '\x1b[36m'
        white = '\x1b[37m'
        default = '\x1b[39m'

        # bright colors based off this: https://gist.github.com/nfejzic/6f3788b3841cb0d7ac11584c6b33b5b9
        class bright:
            black = '\x1b[90m'
            red = '\x1b[91m'
            green = '\x1b[92m'
            yellow = '\x1b[93m'
            blue = '\x1b[94m'
            magenta = '\x1b[95m'
            cyan = '\x1b[96m'
            white = '\x1b[97m'

        rainbow = [
            bright.red,
            yellow,
            bright.yellow,
            bright.green,
            bright.cyan,
            blue,
            magenta
        ]

    class bg:
        black = '\x1b[40m'
        red = '\x1b[41m'
        green = '\x1b[42m'
        yellow = '\x1b[43m'
        blue = '\x1b[44m'
        magenta = '\x1b[45m'
        cyan = '\x1b[46m'
        white = '\x1b[47m'

        class bright:
            black = '\x1b[40m'
            red = '\x1b[41m'
            green = '\x1b[42m'
            yellow = '\x1b[43m'
            blue = '\x1b[44m'
            magenta = '\x1b[45m'
            cyan = '\x1b[46m'
            white = '\x1b[47m'

        rainbow = [
            bright.red,
            yellow,
            bright.yellow,
            bright.green,
            bright.cyan,
            blue,
            magenta
        ]
