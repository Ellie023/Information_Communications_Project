import random #랜덤 번호를 생성하기 위해서 random 모듈 가져오기
import tkinter as tk #gui 구현을 위한 tkinter 모듈 가져오기
from socket import * #소캣 프로그래밍을 위한 socket 모듈을 가져오기 
import _thread #멀티스레딩을 위한 thread 모듈 가져오기

from ETTTP_TicTacToe import TTT, check_msg  # ETTTP_TicTacToe.py의 TTT class와 check_msg class를 가져오기

#변수 name이 main이면 코드 실행
if __name__ == '__main__':

    SERVER_IP = '127.0.0.1' #서버의 ip 주소
    MY_IP = '127.0.0.1' #클라이언트의 ip 주소
    SERVER_PORT = 12000 # 서버의 port 번호
    SIZE = 1024 #데이터를 주고 받을 때 사용할 버퍼크기
    SERVER_ADDR = (SERVER_IP, SERVER_PORT) #접속 정보 설정.서버의 ip 주소와 port 번호를 튜플로 묶어서 저장함 

    
    with socket(AF_INET, SOCK_STREAM) as client_socket: #클라이언트 소캣이라는 이름으로 소캣 생성(IF_IPv4 인터넷 프로토콜 사용, tcp를 위한 소캣)
        client_socket.connect(SERVER_ADDR)  #서버에 연결
        
        ##############################################a#####################
        # Receive who will start first from the server
        start_first=client_socket.recv(SIZE).decode() #서버로부터 선공이 누굴 지 수신함. 데이터로 수신되며, 문자열로 디코딩
        packet=start_first.replace("\r\n"," ").replace(":", " ")#엔터와 ' ;'를 공백으로 바꾼 후 
        packetSplit=packet.split(" ")#공백을 기준으로 나눔

        #메세지가 correct한 지 체크한다 -> 아니면 프로그램 종료
        if not (packetSplit[0]=="SEND"):
            client_socket.close()
            quit()
        if check_msg(start_first, MY_IP):
            client_socket.close()
            quit()

        # 서버에서 누가 먼저 플레이 할 건지 알려줌
        if packetSplit[5]=="ME":#서버가 먼저
            start=0
        elif packetSplit[5]=="YOU": #클라이언트가 먼저 
            start=1
        else:#유효하지 않은 값
            client_socket.close()
            quit()

        ######################### Fill Out ################################
        # Send ACK \
        if(start ==0): #server가 선공, 서버에게 너가 먼저 시작하라는 ack 메세지
            ACK ="ACK ETTTP/1.0\r\nHost:"+SERVER_IP+"\r\nFirst-Move:YOU\r\n\r\n"
        else: #client가 선공, 서버에게 내가 먼저 시작하겠단 ack 메세지
           ACK = "ACK ETTTP/1.0\r\nHost:"+SERVER_IP+"\r\nFirst-Move:ME\r\n\r\n"
        client_socket.send(ACK.encode()) #서버에게 소캣을 통해서 ack 메세지를 보냄
        
        ###################################################################
        
        # Start game
        #젒속한 소캣,client ip 주소, server ip 주소를 매개변수로 넘기고 TTT class 객체 생성
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start) #누가 먼저 시작할지 설정하고 TTT 클래스의 plat 함수 호출, Tic-tac-toe를 시작한다.
        root.mainloop() #tkinter의 메인 이벤트(마우스 클릭) 루프를 실행하여 gui 유지
        client_socket.close() #게임이 끝나면 소켓 닫기 
        
        