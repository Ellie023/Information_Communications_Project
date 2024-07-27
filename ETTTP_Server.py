import random #랜덤 번호를 생성하기 위해서 random 모듈 가져오기
import tkinter as tk #gui 구현을 위한 tkinter 모듈 가져오기
from socket import * #소캣 프로그래밍을 위한 socket 모듈을 가져오기 
import _thread #멀티스레딩을 위한 thread 모듈 가져오기

from ETTTP_TicTacToe import TTT, check_msg  # ETTTP_TicTacToe.py의 TTT class와 check_msg class를 가져오기

#변수 name이 main이면 코드 실행

if __name__ == '__main__':
    
    global send_header, recv_header #전역변수
    SERVER_PORT = 12000 #server의 port 번호 
    SIZE = 1024 #데이터를 주고 받을 때 사용할 버퍼크기
    server_socket = socket(AF_INET,SOCK_STREAM) #서버 소캣 생성(IPv4 인터넷 프로토콜 사용,tcp를 위한 소캣)
    server_socket.bind(('',SERVER_PORT)) #소켓의 주소 할당
    server_socket.listen() #연결 대기 상태
    MY_IP = '127.0.0.1' #서버 ip 주소
    
    #server는 client가 연결을 요청할 때까지 서버를 열어두고 기다린다 
    while True:
        client_socket, client_addr = server_socket.accept() #client의 연결 요청을 수락함
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        #누가 먼저 시작할 지를 정한 SEND 메세지를 작성하고 클라이언트에게 전송한다.
        packet = f"SEND ETTTP/1.0\r\nHost:{client_addr[0]}\r\nFirst-Move:{'ME' if start == 0 else 'YOU'}\r\n\r\n"
        client_socket.send(packet.encode())
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        #누가 먼저 시작할지 메세지가 옴. 바이트 단위의 데이터로 문자가 수신됨
        ACK=client_socket.recv(SIZE).decode()#클라이언트가 보낸 ACK를 데이터에서 문자열로 바꾼다 
        ACK=ACK.replace("\r\n"," ").replace(":", " ") #엔터와 ':'를 공백으로 바꾸고
        AckSplit=ACK.split(" ")#공백을 기준으로 나눈다.

        #ACK 메세지가 correct 한 지 확인한다.
        if not (AckSplit[0]=="ACK"):
            client_socket.close()
            quit()
        if check_msg(ACK, MY_IP):
            client_socket.close()
            quit()


        if(start == 0): #server가 선공
            if not (AckSplit[5]=="YOU"):
                client_socket.close()
        elif(start==1): #client 가 선공
            if not (AckSplit[5]=="ME"):
                client_socket.close()

        ###################################################################
          #젒속한 소캣,client ip 주소, server ip 주소를 매개변수로 넘기고 TTT class 객체 생성
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start) #첫 시작이 누군 지 알려주고 게임이 시작된다.
        root.mainloop() #마우스 클릭 같은 이벤트를 위한 loop 실행. gui 유지
        
        client_socket.close() #게임이 끝나면 소켓 닫기
        
        break
    server_socket.close()