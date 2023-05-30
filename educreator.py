#!/usr/bin/env python3

import sys
import os
import shlex
import shutil
import subprocess

class EduCreator:

    def main(self):

        self.dir = "/tmp/educreator"

        if len(sys.argv) < 2:
            print("specify files")
            quit()

        self.prepare_directory()
        self.prepare_repository()        

        for i in range(1, len(sys.argv)):
            arg = sys.argv[i]

            self.process_file(arg)

    def prepare_directory(self):

        self.script_dir = os.getcwd() + "/"

        try:
            shutil.rmtree(self.dir)
        except FileNotFoundError:
            pass

        try:
            os.mkdir(self.dir, 0o0755);
        except FileExistsError:
            pass

        os.chdir(self.dir)
    
    def prepare_repository(self):
        
        self.exec("git init -b master")
        self.exec("touch .gitignore")
        self.exec("git add .gitignore")
        self.exec("git commit -m 'initial commit'")

    def process_file(self, fnam):

        if not fnam.endswith(".edu"):
            return

        file = open(self.script_dir + fnam, "rt")
        lines = file.readlines()
        file.close()

        resnam = fnam[:-3] + "md"
        self.res = open(self.script_dir + resnam, "w+")

        self.is_inside_cmd = False

        for line in lines:
            line = line.strip()
            self.process_line(line)

        if self.is_inside_cmd:
            self.append_code_block_close()
    
    def process_line(self, line):

        if self.is_inside_cmd:

            if self.is_command(line):
                self.append_exec(line)
            else:
                self.is_inside_cmd = False
                self.append_code_block_close()
                self.append_line(line)
            
        else:

            if self.is_command(line):
                self.is_inside_cmd = True
                self.append_code_block_open()
                self.append_exec(line)
            else:
                self.append_line(line)


    def is_command(self, line):
        if line == "": return False
        return line[0] == '$'

    def append_line(self, line):
        print(line, file=self.res)
    
    def append_code_block_open(self):
        self.append_line("````")

    def append_code_block_close(self):
        self.append_line("````")

    def append_exec(self, line):

        self.append_line(line)

        command = line[1:].strip()
        result = self.exec(command)
        self.append_line(result)

    def exec(self, command):

        cmd_array = shlex.split(command)
        try:
            result = subprocess.check_output(cmd_array)
        except subprocess.CalledProcessError:
            print("ERROR: command failed: " + command)
            quit(1)

        return result        

if __name__ == "__main__":
    try:
        EduCreator().main()
    except KeyboardInterrupt:
        print(" - interrupted")
        quit()
