#!/usr/local/bin/python
from copy import deepcopy
from random import randrange
import os

class WeirdMachine:
    def __init__(self, arg1: int, arg2: int):
        self.MAX_REGISTERS = 10
        self.MAX_COMPUTERS = 10
        self.MAX_VALUE = 1000
        self.MAX_TICKS = 5000
        self.MAX_SCRIPT_LENGTH = 100

        self.computers = [
            {
                'REGISTERS': [arg1, arg2] + [0 for _ in range(self.MAX_REGISTERS - 2)],
                'INSTRUCTIONS': [],
                'IP': 0
            }
        ]
        self.running = False
        self.result = None
        self.ticks = 0


    def parse_instruction(self, computer_idx: int) -> bool:
        """
        Parse and run the instruction. Returns True if successful, False otherwise.
        """
        computer = self.computers[computer_idx]
        instruction = computer['INSTRUCTIONS'][computer['IP']]

        computer['IP'] += 1

        command, arguments = instruction.split(' ')[0], instruction.split(' ')[1:]

        try:
            arguments = [int(arg) for arg in arguments]
        except:
            return False

        if command == "SET":
            if len(arguments) != 2: return False
            register, value = arguments[0], arguments[1]

            if register >= self.MAX_REGISTERS or abs(value) > self.MAX_VALUE: return False

            computer['REGISTERS'][register] = int(value)
            return True

        elif command == "ADD":
            if len(arguments) != 2: return False
            dest, src = arguments[0], arguments[1]

            if src >= self.MAX_REGISTERS or dest >= self.MAX_REGISTERS: return False

            computer['REGISTERS'][dest] += computer['REGISTERS'][src]
            return True

        elif command == "NEG":
            if len(arguments) != 1: return False

            register = arguments[0]

            if register >= self.MAX_REGISTERS or len(self.computers) >= self.MAX_COMPUTERS: return False

            computer_clone = deepcopy(computer)
            computer_clone['REGISTERS'][register] = -computer_clone['REGISTERS'][register]

            self.computers.append(computer_clone)
            
            return True

        elif command == "JIZ":
            if len(arguments) != 2: return False

            register, ip = arguments[0], arguments[1]

            if register >= self.MAX_REGISTERS or ip >= len(computer['INSTRUCTIONS']): return False

            if computer['REGISTERS'][register] == 0:
                computer['IP'] = int(ip)
            
            return True

        elif command == "JNZ":
            if len(arguments) != 2: return False

            register, ip = arguments[0], arguments[1]

            if register >= self.MAX_REGISTERS or ip >= len(computer['INSTRUCTIONS']): return False

            if computer['REGISTERS'][register] != 0:
                computer['IP'] = int(ip)
            
            return True
        
        elif command == "HALT":
            if len(arguments) != 1: return False

            register = arguments[0]
            
            if register >= self.MAX_REGISTERS: return False

            self.result = computer['REGISTERS'][register]
            self.running = False

            return True
            

    def run_script(self, lines: list) -> int or None:
        """
        Runs the script and returns the result.
        """
        self.running = True
        self.result = None
        self.ticks = 0

        for line in lines:
            self.computers[0]['INSTRUCTIONS'].append(line)

        while self.running:
            # Run one instruction for each computer, per tick
            for computer_idx in range(len(self.computers)):
                if self.computers[computer_idx]['IP'] >= len(self.computers[computer_idx]['INSTRUCTIONS']):
                    print("Computer {} has no more instructions to run. Assuming implicit HALT, no results will be returned.".format(computer_idx))
                    self.running = False
                    break

                elif not self.parse_instruction(computer_idx):
                    print("Invalid instruction or error occured: {}".format(self.computers[computer_idx]['INSTRUCTIONS'][self.computers[computer_idx]['IP'] - 1]))
                    self.running = False
                    break
                
                # Return once the first computer halts
                if not self.running:
                    break
            
            self.ticks += 1
            if self.ticks > self.MAX_TICKS:
                print("Max ticks exceeded. Assuming implicit HALT, no results will be returned.")
                self.running = False

        return self.result

    
    def get_script(self):
        """
        Get the script.
        """
        print('===== ENTER YOUR SCRIPT =====')
        result = []
        while len(result) <= self.MAX_SCRIPT_LENGTH:
            line = input()
            if line:
                result.append(line)
            else:
                break

        return result

    
    def reset(self, arg1: int, arg2: int):
        """
        Reset the machine with arg1 and arg2 as the inputs.
        """
        self.computers = [
            {
                'REGISTERS': [arg1, arg2] + [0 for _ in range(self.MAX_REGISTERS - 2)],
                'INSTRUCTIONS': [],
                'IP': 0
            }
        ]
        self.running = False
        self.result = None
        self.ticks = 0

    
    def test(self, range1: tuple, range2: tuple, script: list) -> bool:
        """
        Runs test cases, based on randomly generated values from range1 and range2.
        Returns True if the test case passes, False otherwise.
        """
        print(f"Range: {range1} {range2}")
        for _ in range(100):
            arg1, arg2 = randrange(*range1), randrange(*range2)
            self.reset(arg1, arg2)
            result = self.run_script(script)

            if result != arg1 * arg2:
                print("Test case failed! Try harder")
                return False
        return True

    
    def main(self):
        """
        Main function.
        """
        print("Sample test case: 5 * -5 = -25")
        self.reset(5, -5)
        script = self.get_script()

        result = self.run_script(script)
        print("========== RESULT ===========")
        print("Result: {}".format(result))
        print('============ END ============')

        if result == -25:
            print("Sample test case passed. Good job! Beginning to evaluate real test cases.")
            print('========== TESTING ==========')

            if all((
                self.test((0, self.MAX_VALUE), (0, self.MAX_VALUE), script),
                self.test((-self.MAX_VALUE, 0), (0, self.MAX_VALUE), script),
                self.test((0, self.MAX_VALUE), (-self.MAX_VALUE, 0), script),
                self.test((-self.MAX_VALUE, 0), (-self.MAX_VALUE, 0), script),
                self.test((-self.MAX_VALUE, self.MAX_VALUE), (-self.MAX_VALUE, self.MAX_VALUE), script)
            )):
                print("All test cases passed. Good job!")
                print("Here's your flag:", os.environ.get('FLAG'))
            else:
                print("Some test cases failed. Try harder.")

        else:
            print("Sample test case failed. Try harder!")

    print('============ END ============')


if __name__ == '__main__':
    weird_machine = WeirdMachine(0, 0)
    weird_machine.main()