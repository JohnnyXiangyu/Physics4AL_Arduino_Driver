import msvcrt
print('Loading input module ...')


class usrInput:
    '''
    User input object, windows version (Msvcrt)
    should maintain the following API on transplanted platforoms: 
        getInput(): return 1 for red button (EVENT button)
                    return 2 for black button (EXIT button)
    '''

    def getInput(self):
        '''action per frame, return 1 for red button and 2 for black button'''
        if msvcrt.kbhit():
            char = msvcrt.getwch()
            if char == 'q' or char == 'Q':
                return 2
            elif char == 'e' or char == 'E':
                return 1
            else:
                return 0
        else:
            return -1
            