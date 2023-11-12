class FA:
    def __init__(self):
        self.states = list[str]([])
        self.initial = int(0)
        self.finals = list[int]([])
        self.transitions = list[tuple[int, int, str]]([])

    @staticmethod
    def from_file(filename: str) -> 'FA':
        file = open(filename, 'r', encoding='utf-8')
        result = FA()

        states_str = file.readline()[:-1]
        result.states.extend(states_str.split())

        initial_str = file.readline()[:-1]
        result.initial = result.states.index(initial_str)

        finals_str = file.readline()[:-1]
        result.finals.extend([result.states.index(final_str) for final_str in finals_str.split()])

        transitions_strs = file.readlines()
        for transition_str in transitions_strs:
            initial_str, final_str, name = transition_str[:-1].split(' ', 2)
            result.transitions.append((result.states.index(initial_str), result.states.index(final_str), name))

        return result

    def __str__(self) -> str:
        result = ''

        result += 'States: '
        for state in self.states:
            result += state + ' '
        result += '\n'

        result += 'Alphabet: '
        for transition in self.transitions:
            result += transition[2] + ' '
        result += '\n'

        result += 'Initial state: ' + self.states[self.initial] + '\n'

        result += 'Final states: '
        for final in self.finals:
            result += self.states[final] + ' '
        result += '\n'

        result += '\nTransitions:\n'
        for transition in self.transitions:
            result += f'Name: {transition[2]}, From: {self.states[transition[0]]}, To: {self.states[transition[1]]}\n'

        return result

    def verify(self, value: str) -> bool:
        stack = [(-1, self.initial, ''), ]
        def key(t): return str(t[2]) + str(t[0] * len(self.transitions) + t[1])

        index = 0
        invalid = None
        while len(stack) != 0:
            if index >= len(value):
                if stack[-1][1] in self.finals:
                    return True
                else:
                    invalid = stack.pop()

            prev = stack[-1]
            transitions = sorted(
                list(filter(
                    lambda t: (t[0] == prev[1]) and (True if invalid is None else key(t) > key(invalid)),
                    self.transitions
                )),
                key=key
            )

            for transition in transitions:
                try:
                    if value[index:].index(transition[2]) == 0:
                        stack.append(transition)
                        index += len(transition[2])
                        invalid = None
                        break
                except ValueError:
                    continue
            else:
                invalid = stack.pop()
                index -= len(invalid[2])

        return False
