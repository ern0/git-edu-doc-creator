#!/usr/bin/env python3

import sys

class EduCreator:

    def main(self):

        if len(sys.argv) < 2:
            print("specify files")
            quit()

        for i in range(1, len(sys.argv)):
            arg = sys.argv[i]

            self.process_file(arg)


    def process_file(self, fnam):

        if not fnam.endswith(".edu"):
            return

        file = open(fnam, "rt")
        lines = file.readlines()
        file.close()

        resnam = fnam[:-3] + "md"
        self.res = open(resnam, "w+")

        for line in lines:
            line = line.strip()

            self.process_line(line)
    
    def process_line(self, line):

        print(line, file=self.res)

if __name__ == "__main__":
    try:
        EduCreator().main()
    except KeyboardInterrupt:
        print(" - interrupted")
        quit()
