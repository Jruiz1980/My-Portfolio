import os
import queue

SCHEDULE = 1
ATTEND = 2
QUIT = 0

def display_menu():
    os.system('cls')
    print(f'''                                      My Calendar
{SCHEDULE}.- Schedule event
{ATTEND}.- Attend event
{QUIT}.- Quit''')

def schedule_event(ag):
    print('                                         Schedule Event')
    event = input('Event: ')
    ag.put(event)

def attend_event(ag): 
    print('                                         Attend Event')
    if ag.empty():
        print('No events to attend')
    else:
        event = ag.get()
        print(f'Event: {event}')

def main():
    calendar = queue.PriorityQueue()
    forward = True
    while forward:
        display_menu()
        opc = int(input('Select an option: '))
        os.system('cls')
        if opc == SCHEDULE:
            schedule_event(calendar)
        elif opc == ATTEND:
            attend_event(calendar)
        elif opc == QUIT:
            forward = False
        else:
            print('Invalid option...')
        input('Pres ENTER to continue...')
    print('Good-Bye')

if __name__ == '__main__':
    main()