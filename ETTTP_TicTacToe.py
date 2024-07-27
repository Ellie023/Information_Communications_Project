
import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
           #객체 생성하고 값 초기화
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
       
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')#창 사이즈

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr #목적지 ip
        self.recv_ip = src_addr #송신자의 ip
        
        self.total_cells = 9 
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
       #client의 경우
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-01-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"YOU"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"ME"}   
        #server의 경우
        else:
            self.myID = 0
            self.title('34743-01-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

        #보드의 배경색
        self.board_bg = 'white'
        #이기는 경우
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self): #quit 버튼 만들기
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        #프레임을 생성해하고 제어 프레임을 창 위쪽에 배치
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):  #hold/ready 표시하는 함수  
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self): #결과 표시 ui
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self): # edbug 를 입력받음
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):#결과 표시하는 ui
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1): #프로그램 시작
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID: #선공 플레이어
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0 # 후공 플레이어
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self): #프로그램을 닫음
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move): #ui에서 클릭한 부분 인식
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        #이미 선택된 부분/ 자기 turn이 아님
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        #입력받은 값을 send_move 함수로 보낸다. 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid: #ack 메세지가 안 오는 등의 문제로 false면
            self.quit() #프로그램 종료
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move) #보드에 표시 
        
        # If the game is not over, change turn
        #게임이 끝난 게 아니라서 turn을 넘겨준다.
        if self.state == self.active:    
            self.my_turn = 0 #자신의 차레가 아님을 나타냄
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']  #hold 띄우기
            _thread.start_new_thread(self.get_move,()) #프로그램이 중단되는 것을 방지
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self): #상대방이 보낸 move 메세지를 확인하고 자신의 보드에 표시 후 ack를 전송하는 함수
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        #상대방이 보낸 좌표를 decode 후 메세지가 유효한 지 확인한다.
        msg = self.socket.recv(SIZE).decode()
        if  check_msg(msg, self.recv_ip): # Message is not valid
            self.socket.close() #소캣을 닫고    
            self.quit() # 프로그램을 종료시킨다.
            
        else:  # If message is valid - send ack, update board and change turn

            #메세지에서 ':' ',' '괄호', '엔터' 를 공백으로 바꾸고 공백을 기준으로 나누어 준다.
            msg=msg.replace("\r\n", " ").replace(":", " ").replace("("," ").replace(")", " ").replace(",", " ")
            msgSplit=msg.split(" ")
            #'send_ip'와 좌표의 숫자 부분 즉 msgSplit[6] - 행 ,msgSplit[7] -열을 포함하여 ack 메세지를 보낸다. 
            # 당신이 보낸 메세지 잘 받았어
            movingACK="ACK ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nNew-Move:(" + msgSplit[6] + "," + msgSplit[7] + ")\r\n\r\n"
            self.socket.send(movingACK.encode()) #만든 문자열을 인코딩해서 소캣을 통해서 보낸다.
            row = int(msgSplit[6]) #행
            col=int(msgSplit[7]) #열
            loc=3*row+col #표시되는 번호(0-8)
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            #상대 방의 움직음을 보드에 표시하고 아직 게임이 안 끝났으면 turn 넘겨받음
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
    #debug 창에 입력했을 때 메세지 보내고 ack 받고 표시하기
    def send_debug(self):

        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn: #내 차례가 아님 -> 삭제하고 리턴
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end") #메세지를 d_msg에 저장
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end") #텍스트 박스 내용 석재
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        #입력받은 메세지가 correct한지 확인 SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:(1,2)\r\n\r\n
        if check_msg(d_msg, self.send_ip):
            self.socket.close()
            quit()
            return
        # 엔터, ,'',':'를 공백으로 바꾸고 공백을 기준으로 나눔    
        d_msg_Split =d_msg.replace("\r\n"," ").replace(":", " ").split(" ")
        if not (d_msg_Split[0]=="SEND"):
            self.socket.close()
            quit()
            return
        if not (d_msg_Split[2]=="Host"):
            self.socket.close()
            quit()
            return
        if not (d_msg_Split[4]=="New-Move"):
            self.socket.close()
            quit()
            return       

        #좌표 도출하고 숫자만 빼기 작업 
        loc_before=d_msg_Split[5]

        locSplit=loc_before.replace("(", "").replace(")", "").replace(",", " ")
        loc_after=locSplit.split(" ")
        
        row=int(loc_after[0]) #행
        col=int(loc_after[1]) #열

        if not (0<=row<=2 and 0<=col<=2): #보드의 범위가 아님
            return 
        loc=3*row +col #클릭되는 보드의 번호(0-8)
        if(self.board[loc]): #클릭된 상태면
            return
        '''
        Send message to peer
        '''
        #입력받은 메세지를 상대방에게도 전송
        self.socket.send(d_msg.encode())
        '''
        Get ack
        '''
        # 상대방에게서 ACK 받음
        ack_msg=self.socket.recv(SIZE).decode()
        if check_msg(ack_msg,self.recv_ip): #형식에 맞지 않으면 프로그램 종료
            self.socket.close()
            quit()
      # peer's move, from 0 to 8

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
       #보드애 표시하고 게임이 안 끝났으면 Turn을 넘겨줌
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection): #메세지를 보내는 함수
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################
        rowStr=str(row)
        colStr=str(col)
        # send message and check ACK
        msg = "SEND ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nNew-Move:(" + rowStr + "," + colStr + ")\r\n\r\n "
        self.socket.send(msg.encode()) #socket을 통해서 메세지 보내기
        ACK_RECV=self.socket.recv(SIZE).decode() #ACK를 받음
        if check_msg(ACK_RECV, self.recv_ip): #ack가 형식에 맞지 않으면 프로그램 종료
            self.socket.close()
            quit()

        return True
        ######################################################  

    
    def check_result(self,winner,get=False): #결과 확인하기
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
       #winner에서 게임이 종료 됐으므로 winner부터
        if get ==False:
            #진 사람에게 내가 이겼다는 메세지를 보냄
            self.socket.send(("RESULT ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nWinner:ME\r\n\r\n").encode())
            #ack 받고 확인함
            rev_ack=self.socket.recv(SIZE).decode()
            if check_msg(rev_ack, self.recv_ip):
                return False
        elif get==True: #loser의 입장
            #이겼다는 메세지를 받음
            rev_ack =self.socket.recv(SIZE).decode()
            #메세지 유효성 검사
            if check_msg(rev_ack,self.recv_ip): 
                return False
            rev_ack=rev_ack.replace("\r\n"," ").replace("\r\n", " ").split(" ")
            if (rev_ack[5]=="ME"):
                return False
           #ack 메세지 보내기
            self.socket.send(("RESULT ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nWinner:YOU\r\n\r\n").encode())
            
        else:
            return False    

        return True
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False): #보드에 표시하기
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip): #전송받은 메세지의 유효성 검사 
    '''

    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    #엔터랑 ':'를 공백으로 바꾸고 공백으로 나눈다
    msg_after=msg.replace("\r\n"," ").replace(":"," ")
    msg_arr=msg_after.split(" ")
 # Ensure that the message has at least the minimum required parts
    if msg_arr[1] != "ETTTP/1.0": #프로토콜이 잘못됨
        print("Protocol error") 
        return True
    
    if msg_arr[3] != str(recv_ip): #수신 ip 주소가 잘못됨
        print("IP address error")
        return True


    return False  
    ######################################################  