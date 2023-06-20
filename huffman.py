import heapq
import os
class BinaryTreeNode:
    def __init__(self,value,frequency):
        self.value=value
        self.frequency=frequency
        self.left=None
        self.right=None

    def __lt__(self,other):
        return self.frequency<other.frequency
    def __eq__(self,other):
        return self.frequency==other.frequency
    
class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}
        self.__reverseCodes={}
    def __make_frequency_dict(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            freq_dict[char]+=1
        return freq_dict
    
    def __build_heap(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            binary_tree_node=BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binary_tree_node)

    def __buildTree(self):
        while len(self.__heap)>1:
            node_1=heapq.heappop(self.__heap)
            node_2=heapq.heappop(self.__heap)
            new_frequency=node_1.frequency+node_2.frequency
            newNode=BinaryTreeNode(None,new_frequency)
            newNode.left=node_1
            newNode.right=node_2
            heapq.heappush(self.__heap,newNode)
        return
    def __buildCodesHelper(self,root,currentBit):
        if root is None:
            return
        if root.value is not None:
            self.__codes[root.value]=currentBit
            self.__reverseCodes[currentBit]=root.value
            return
        self.__buildCodesHelper(root.left,currentBit+"0")
        self.__buildCodesHelper(root.right,currentBit+"1")
    def __buildCodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildCodesHelper(root,"")

    def __getEncodedText(self,text):
        encode_text=""
        for char in text:
            encode_text+=self.__codes[char]
        return encode_text
    
    def __getPaddedEncodedText(self,encoded_text):
        padded_amaount=8-len(encoded_text)%8
        for i in range(padded_amaount):
            encoded_text+="0"

        padded_info="{0:08b}".format(padded_amaount)
        padded_encoded_text=padded_info+encoded_text
        return padded_encoded_text
    
    def __getBytesArray(self,padded_text):
        bytesArray=[]
        for i in range(0,len(padded_text),8):
            byte=padded_text[i:i+8]
            bytesArray.append(int(byte,2))
        return bytesArray
    
    def compress(self):
        #1- get file from the path
        #2- read text from the file
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+".bin"

        with open(self.path,'r+') as file, open(output_path,'wb') as output:
            #3- make frequency dictionary from the text
            text=file.read()
            text=text.rstrip()
            frequecy_dict=self.__make_frequency_dict(text)

            #4- construct the heap from the frequency_dict
            self.__build_heap(frequecy_dict)

            #5- construct the binary tree from the heap
            self.__buildTree()

            #6- construct the codes from the binary tree
            self.__buildCodes()

            #7- creathe the encoded codes from the text
            encoded_text=self.__getEncodedText(text)

            #8- pad the encoded text
            padded_encoded_text=self.__getPaddedEncodedText(encoded_text)
            bytes_array=self.__getBytesArray(padded_encoded_text)
            finaly_bytes=bytes(bytes_array)

            #9- put the encoded text in the binary file and return the binary file
            output.write(finaly_bytes)
        print("compressed")
        return output_path
    
    def __removePadding(self,string):
        padded_info=string[:8]
        extra_padding=int(padded_info,2)
        string=string[8:]
        string_after_padding_removed=string[:-1*extra_padding]
        return string_after_padding_removed
    
    def __decodeText(self,text):
        decodedText=""
        currentBit=""
        for bit in text:
            currentBit+=bit
            if currentBit in self.__reverseCodes:
                decodedText+=self.__reverseCodes[currentBit]
                currentBit=""
        return decodedText
    
    def decompress(self,binPath):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+"_decompressed"+".txt"
        with open(binPath,'rb') as file, open(output_path,'w') as output:
            bitString=''
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bitString+=bits
                byte=file.read(1)
            actual_text=self.__removePadding(bitString)
            decompressed_text=self.__decodeText(actual_text)
            output.write(decompressed_text)

path="Enter the file Path Here"
h=HuffmanCoding(path)
output_path=h.compress()
h.decompress(output_path)

