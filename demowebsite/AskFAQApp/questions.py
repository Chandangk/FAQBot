class Freq:

    def __init__(self,question,answer):
        self.question=question
        self.answer=answer

    def display(self):
        print("Question:"+self.question+" Answer:"+self.answer)

    def getQuestion(self):
        return self.question


FreqList= []

FreqList.append(Freq("asdasdad","ans")) 
FreqList.append(Freq("asdasdad","ans"))
FreqList.append(Freq("asdasdad","ans"))
FreqList.append(Freq("asdasdad","ans"))
FreqList.append(Freq("asdasdad","ans"))
FreqList.append(Freq("asdasdad","ans"))


for freobj in FreqList:
    print("index "+str(FreqList.index(freobj))+" question "+freobj.question+" answer "+freobj.answer)
