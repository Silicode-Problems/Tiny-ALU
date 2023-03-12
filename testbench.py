# Simple tests for an ALU module

import cocotb
from cocotb.triggers import Timer
import random
import wavedrom
import json

def func(a,b,op):
    if(op==0):
        return a
    
    if(op==1):
        return a+b
    if(op==2):
        x = a-b
        if(x>=0):
            return x
        else:
            y=0
            arr=[]
            for i in range(16):
                #y= (y<<1) + (x%2)
                arr.append(x%2)
                x=x>>1
            for i in range(16):
                y=y*2 + arr[15-i]
            return y
    if(op==3):
        return a*b
    if(op==4):
        return a&b
    if(op==5):
        return a|b
    if(op==6):
        return a^b
    if(op==7):
        x = ~a
        y=0
        arr=[]
        for i in range(16):
            #y= (y<<1) + (x%2)
            arr.append(x%2)
            x=x>>1
        for i in range(16):
            y=y*2 + arr[15-i]
        return y
    else: 
        return 0
    

def TransformContinousString(s):
    transformed_str = ""
    for i in range(len(s)-1, 0, -1):
        if s[i] == s[i-1]:
            transformed_str = "." + transformed_str
        else:
            transformed_str = s[i] + transformed_str
    transformed_str = s[0] + transformed_str
    return transformed_str


@cocotb.test()
async def alu_basic_test(dut):
    """Test for 5 , 10"""
    res = 1
    a = 5
    b = 10

    # input driving
    dut.reset.value = res
    dut.A.value = a
    dut.B.value = b
    dut.op_code.value = 2

    await Timer(2, units='ns')

    assert dut.out.value == 0, f"ALU result is incorrect: {dut.out.value} != 0"


@cocotb.test()
async def adder_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""

    data = {'signal1': [], 'signal2': [], 'signal3':[]}
    myoutput = []
    myInput1 = []
    myInput2 = []
    myInput3 = []
    Exp_output = []
    timeString = ""
    equalString = ""
    Mismatch_string = ""

    for i in range(25):
        
        if i > 0:
            timeString += "."
        equalString += "="
        
        res = 0
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        operation = random.randint(0,7)

        dut.reset.value = res
        dut.A.value = a
        dut.B.value = b
        dut.op_code.value = operation
        
        myInput1.append(int(a))
        myInput2.append(int(b))
        myInput3.append(int(operation))
        Exp_output.append(int(func(a,b,operation)))

        await Timer(2, units='ns')

        myoutput.append(int(dut.out.value))
        if (int(dut.out.value) == func(a,b,operation)):
            Mismatch_string+='0'
           
        else:
            Mismatch_string+='1'

        data['signal1'].append([int(dut.A.value), int(dut.B.value)])
        data['signal2'].append(int(dut.out.value))
        data['signal3'].append(int(dut.op_code.value))

        #dut._log.info(f'A={a:05} B={b:05} Operation={operation:03} model={func(a,b,operation):05} DUT={int(dut.out.value):05}')
        #assert dut.out.value == func(a,b,operation), "Randomised test failed with: {A} {C} {B} = {OP}".format(
            #A=dut.A.value, B=dut.B.value, C=dut.op_code.value, OP=dut.out.value)


    json_data = json.dumps(data)
    print(json_data)
    with open("data.json", "w") as f:
        json.dump(data, f)
    print(myInput1, myInput2, myoutput, dut)


    # wd = waveDrom()
    s = " "
    Input1_string = s.join([str(elem) for elem in myInput1])
    Input2_String = s.join([str(elem) for elem in myInput2])
    Input3_string = s.join([str(elem) for elem in myInput3])
    Output_String = s.join([str(elem) for elem in myoutput])
    Exp_output_String = s.join([str(elem) for elem in Exp_output])
    Mismatch_string=TransformContinousString(Mismatch_string)
    print(equalString, timeString)
    # print(Input1_string,"\n",Input2_String,"\n",Output_String)
    data = {
        "signal": [
            {"name": "Clk", "wave": "P"+timeString},
            {"name": "Signal1",  "wave": equalString, "data": Input1_string},
            {"name": "Signal2",  "wave": equalString, "data": Input2_String},
            {"name": "Signal3",  "wave": equalString, "data": Input3_string},
            {"name": "Output",  "wave": equalString, "data": Output_String},
            {"name": "Exp_Output",  "wave": equalString, "data": Exp_output_String},
            {"name": "Mismatch",  "wave": Mismatch_string }




        ]
    }
    data_str = json.dumps(data)
    svg = wavedrom.render(data_str)
    svg.saveas("demo1.svg")        