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

        if line == "":
            self.append_line("")
            return

        if self.is_inside_cmd:

            if self.is_starting_with_dollar(line):
                self.append_exec(line)
            else:
                self.is_inside_cmd = False
                self.append_code_block_close()
                self.append_line(line)
            
        else:

            if self.is_starting_with_dollar(line):
                self.is_inside_cmd = True
                self.append_code_block_open()
                self.append_exec(line)
            else:
                self.append_line(line)

    def is_starting_with_dollar(self, line):
        if line == "": return False
        return line[0] == '$'

    def append_line(self, line):

        if self.is_inside_cmd:
            self.code_block.append(line)
        else:
            self.append_raw_line(line)
    
    def append_raw_line(self, line):
        print(line, file=self.res)
    
    def append_code_block_open(self):
        self.code_block = []

    def append_code_block_close(self):

        cb_len = len(self.code_block)

        if cb_len == 0:
            return
    
        if self.code_block[cb_len - 1] == "":
            del self.code_block[cb_len - 1]
        
        self.append_raw_line("```")

        for line in self.code_block:
            self.append_raw_line(line)

        self.append_raw_line("```")

    def append_exec(self, line):

        command = line[1:].strip()

        if self.is_starting_with_dollar(command):
            suppress_output = True
            command = command[1:].strip()
        else:
            suppress_output = False
            self.append_line(line)

        result = self.exec(command)

        if suppress_output:
            return
        res_chr = result.decode("utf-8")
        if res_chr.strip() == "":
            return
        
        self.append_cmd_result(res_chr)
    
    def exec(self, command):

        cmd_eff = ["/bin/bash", "-c", command]
        try:
            result = subprocess.check_output(cmd_eff)
        except subprocess.CalledProcessError:
            print("ERROR: command failed: " + command)
            quit(1)

        return result        

    def append_cmd_result(self, result):

        if result.endswith("\n"):
            result = result[:-1]

        res_arr = result.split("\n")
        for res in res_arr:
            self.code_block.append(res)

if __name__ == "__main__":
    try:
        EduCreator().main()
    except KeyboardInterrupt:
        print(" - interrupted")
        quit()
