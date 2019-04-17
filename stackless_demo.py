# this is a demo for showing how to use stackless python to send & receive pkt

import stackless as stk
import socket,time

st_result = []
send_chnl = stk.channel()
rcvd_chnl = stk.channel()

def sendtry(des):
    if rcvd_chnl.receive():
        pass
    print('send begin ', des)

    pass

    send_chnl.send(des)
    # print('continue send')
    # rcv = rcvd_chnl.receive()
    # print(rcv)

    # send_chnl.send(rcvd_chnl.receive())
    print('the send ',des,'end')
def rcvtry():
    print('rcv thread begin ')
    while 1:
        # print('rcv again ')
        r = send_chnl.receive()
        print('rcvd the chnl, start listening',end=' ')
        while 1:
            print('r: ',r)
            print('listen finished, send the chnl to next thread')
            rcvd_chnl.send('rcv chnl')
            break
        print('rcv once')
stk.tasklet(rcvd_chnl.send)('d')
stk.tasklet(sendtry)(123)
stk.tasklet(sendtry)(144)
# stk.tasklet(oo)(123)
stk.tasklet(rcvtry)()
# stk.tasklet(rcvtry)()

stk.run()