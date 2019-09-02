from tkinter import *
from datetime import *
import imaplib, email, os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

root = Tk()
root.title('Admin Portal')


bgpic = PhotoImage(file="bgpic.png")
bglabel = Label(root,image=bgpic)
bglabel.place(anchor=CENTER,relx=0.5,rely=0.43)

cr = PhotoImage(file="cc.png")
crlabel = Label(root,image=cr)
crlabel.place(anchor=CENTER,relx=0.89,rely=0.82)

user=Label(root,text='Username: ',fg='blue',bg='white',font=('Comic Sans MS',17,'bold')).place(relx=0.38,rely=0.4,anchor=CENTER)
e1=Entry(root,bg='white',fg='black',relief=SUNKEN)
e1.place(relx=0.48,rely=0.404,anchor=CENTER)
pas=Label(root,text='Password: ',fg='blue',bg='white',font=('Comic Sans MS',17,'bold')).place(relx=0.38,rely=0.48,anchor=CENTER)
e2 = Entry(root,bg='white',fg='black',show='*',relief=SUNKEN)
e2.place(relx=0.48,rely=0.484,anchor=CENTER)


def get_input():
    #you can define your own user id and password below to log in to the portal
    if (e1.get()=='admin') and (e2.get()=='admin'):
        
        e1.delete(0,END)
        e2.delete(0,END)
        root.destroy()
        portal=Tk()
        portal.title('Dashboard')
        now=datetime.now()
        Label(portal,text=now.strftime("%a,%d,%B,%Y"),font=('Comic Sans MS',17,'bold')).place(anchor=CENTER,relx=0.09,rely=0.06)
        Label(portal,text='Welcome to the dashboard. Select option from below:',fg='red',bg='white',font=('Times',20,'bold')).place(anchor=CENTER,relx=0.48,rely=0.28)

        def auth(user,password,imap_url):
            con = imaplib.IMAP4_SSL(imap_url)
            con.login(user,password)
            return con

        def get_body(msg):
            if msg.is_multipart():
                return get_body(msg.get_payload(0))
            else:
                return msg.get_payload(None,True)
        def qwindow():
            q=Tk()
            q.title('Query Window')
            
            

            #write the email id for queries
            user = ''
            #write password
            password = ''
            imap_url = 'imap.gmail.com'

            con1 = auth(user,password,imap_url)
            con1.select('INBOX')

            type, data = con1.search(None, 'ALL')

            mail_ids = data[0]
            id_list = mail_ids.split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            
            list_date=Listbox(q,width=30,height=30)
            list_subject=Listbox(q,width=30,height=30)
            list_name=Listbox(q,width=20,height=30)
            list_email=Listbox(q,width=30,height=30)
            list_query=Listbox(q,width=50,height=30)

            
            list_date.insert(1,'S.N.                DATE')
            list_subject.insert(1,'                    SUBJECT')
            list_name.insert(1,'NAME')
            list_email.insert(1,'                    EMAIL')
            list_query.insert(1,'                                       QUERY')

            
            list_date.insert(2,' ')
            list_subject.insert(2,' ')
            list_name.insert(2,' ')
            list_email.insert(2,' ')
            list_query.insert(2,' ')

            
            list_date.itemconfig(0,{'fg':'blue'})
            list_subject.itemconfig(0,{'fg':'blue'})
            list_name.itemconfig(0,{'fg':'blue'})
            list_email.itemconfig(0,{'fg':'blue'})
            list_query.itemconfig(0,{'fg':'blue'})

            msg_array=[]
            
            for i in range(latest_email_id,first_email_id-1, -1):
                
                typ, data = con1.fetch(str(i), '(RFC822)')
                
                raw = email.message_from_bytes(data[0][1])

                s=str(get_body(raw))
                s=s.replace('\\r\\n\\r\\n','\n')
                s=s[2:-6]
                a=s.split('\n')
                sn=latest_email_id-i+3
                t=raw['date']
                t=t[:-5]

                msg_array.append(a[-1])
                
                list_date.insert(sn,' '+str(sn-2)+'|    '+t)
                list_subject.insert(sn,raw['Subject'])
                list_name.insert(sn,str(sn-2)+'. '+a[0][6:])
                list_email.insert(sn,str(sn-2)+'. '+a[1][8:])
                list_query.insert(sn,str(sn-2)+'. '+a[-1])
                #print('Date: ',t)
                #print('Subject: ',raw['Subject'])
                #print(s)

                #print('-------------------')



            

            Label(q,text='DATA TABLE',fg='orange',bg='white',font=('Times',20,'bold')).grid(row=1,column=3)
            Label(q,text='Enter the S.N. of the query\n you want to view :',font=('Times',12,'bold'),bg='white').place(anchor=CENTER,relx=0.84,rely=0.2)

            qno=Entry(q,bg='white',relief=SUNKEN,width=10)
            qno.place(anchor=CENTER,relx=0.84,rely=0.25)
            
    
            def view_query():
                if(qno.get()==''):
                    p1=Tk()
                    Label(p1,text='Enter Serial Number !',fg='red',bg='white').pack()
                    Button(p1,text="OK",command=p1.destroy).pack()
                    p1.configure(background='white')
                    p1.mainloop()
                elif(int(qno.get())<1 or int(qno.get())>len(msg_array)):
                    p2=Tk()
                    Label(p2,text='Invalid Serial Number !',fg='red',bg='white').pack()
                    Button(p2,text="OK",command=p2.destroy).pack()
                    p2.configure(background='white')
                    p2.mainloop()
                else:
                    qry_msg=Tk()
                    Label(qry_msg,text=msg_array[int(qno.get())-1],bg='white',relief='groove',wraplength=300,font=('Times',13)).pack(side=TOP)
                    Button(qry_msg,text='Close',fg='white',bg='black',font=('Times',10),command=qry_msg.destroy).pack(side=BOTTOM)
                    qry_msg.configure(background='white')
                    qry_msg.mainloop()
            
            Button(q,text='View Query',fg='black',bg='white',command=view_query).place(anchor=CENTER,relx=0.84,rely=0.3)   


            def reply_query():
                reply=Tk()
                em=Label(reply,text=' Email :',fg='black',bg='white',font=('Times',14,'bold')).place(anchor=CENTER,relx=0.36,rely=0.2)
                em_entry=Entry(reply,relief=SUNKEN,width=35,bd='3',font=('Times',12))
                em_entry.place(anchor=CENTER,relx=0.51,rely=0.2)
                mg=Label(reply,text='Message : ',fg='black',bg='white',font=('Times',14,'bold')).place(anchor=CENTER,relx=0.37,rely=0.3)
                 
                mg_txt=Text(reply,height=7,width=45,bd='4',font=('Times',12))
                mg_txt.place(anchor=CENTER,relx=0.51,rely=0.42)
                scrl=Scrollbar(reply,orient='vertical')   
                scrl.place(relx=0.644,rely=0.326,relheight=0.19)
                scrl.config(command=mg_txt.yview)
                mg_txt.config(yscrollcommand=scrl.set)


                def send():
                    if(em_entry.get()=='' or mg_txt.get('1.0',END)==' '):
                        pb=Tk()
                        Label(pb,text='Enter Data!',fg='red',bg='white').pack()
                        Button(pb,text='OK',fg='black',bg='white',command=pb.destroy).pack()
                        pb.configure(background='white')
                        pb.mainloop()

                    else:
                        try:
                            server=smtplib.SMTP('mail.smtp2go.com',2525)
                            #enter your smpt2go mail account and password
                            smtpmail=''
                            smtppass=''
                            server.login(smtpmail,smtppass)
                            msg = MIMEMultipart()
                            msg['Subject'] = "Reply To Query at RPSC"
                            body = mg_txt.get("1.0",END)
                            msg.attach(MIMEText(body, 'plain'))
                            text = msg.as_string()
                            
                            server.sendmail(smtpmail,em_entry.get(),text)
                            em_entry.delete(0,END)
                            mg_txt.delete('1.0',END)
                            prompt=Tk()
                            Label(prompt,text='MESSAGE SUCCESSFULY SENT!',fg='red',bg='white').pack()
                            Button(prompt,text='OK',fg='black',bg='white',command=prompt.destroy).pack()
                            prompt.configure(background='white')
                            prompt.mainloop()
                        except:
                            
                            p4=Tk()
                            Label(p4,text='Mail not sent. Try again\nor check email address!',fg='red',bg='white').pack()
                            Button(p4,text='OK',fg='black',bg='white',command=p4.destroy).pack()
                            p4.configure(background='white')
                            p4.mainloop()
                    


                Button(reply,text='Exit',bg='red',fg='white',font=('Times',12),command=reply.destroy).place(anchor=CENTER,relx=0.65,rely=0.75)
                Button(reply,text='Send',bg='blue',fg='white',font=('Times',14,'bold'),command=send).place(anchor=CENTER,relx=0.52,rely=0.56)
                reply.geometry('1500x1500')
                reply.configure(background='white')
                reply.mainloop()


            Button(q,text='Quit Window',fg='white',bg='red',font=('Times',14),command=q.destroy).place(anchor=CENTER,relx=0.52,rely=0.8)
            Button(q,text='Reply to a Query',fg='white',bg='green',font=('Times',14,'bold'),command=reply_query).place(anchor=CENTER,relx=0.4,rely=0.8)
              
            list_date.grid(row=2,column=1) 
            list_subject.grid(row=2,column=2)
            list_name.grid(row=2,column=3)
            list_email.grid(row=2,column=4)
            list_query.grid(row=2,column=5)
            q.configure(background='white')
            q.geometry('1500x1500')
            q.mainloop()



        def fwindow():
            f=Tk()
            f.title('Feedback Window')
            
            

            #write the email id for feedback
            user = ''
            #write password
            password = ''
            imap_url = 'imap.gmail.com'

            con1 = auth(user,password,imap_url)
            con1.select('INBOX')

            type, data = con1.search(None, 'ALL')

            mail_ids = data[0]
            id_list = mail_ids.split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            
            list_date=Listbox(f,width=30,height=30)
            list_subject=Listbox(f,width=30,height=30)
            list_name=Listbox(f,width=20,height=30)
            list_email=Listbox(f,width=30,height=30)
            list_feedback=Listbox(f,width=50,height=30)

            
            list_date.insert(1,'S.N.                DATE')
            list_subject.insert(1,'                    SUBJECT')
            list_name.insert(1,'NAME')
            list_email.insert(1,'                    EMAIL')
            list_feedback.insert(1,'                                   FEEDBACK')

            
            list_date.insert(2,' ')
            list_subject.insert(2,' ')
            list_name.insert(2,' ')
            list_email.insert(2,' ')
            list_feedback.insert(2,' ')

            
            list_date.itemconfig(0,{'fg':'blue'})
            list_subject.itemconfig(0,{'fg':'blue'})
            list_name.itemconfig(0,{'fg':'blue'})
            list_email.itemconfig(0,{'fg':'blue'})
            list_feedback.itemconfig(0,{'fg':'blue'})

            msg_array=[]
            
            for i in range(latest_email_id,first_email_id-1, -1):
                
                typ, data = con1.fetch(str(i), '(RFC822)')
                
                raw = email.message_from_bytes(data[0][1])

                s=str(get_body(raw))
                s=s.replace('\\r\\n\\r\\n','\n')
                s=s[2:-6]
                a=s.split('\n')
                sn=latest_email_id-i+3
                t=raw['date']
                t=t[:-5]

                msg_array.append(a[-1])
                
                list_date.insert(sn,' '+str(sn-2)+'|    '+t)
                list_subject.insert(sn,raw['Subject'])
                list_name.insert(sn,str(sn-2)+'. '+a[0][6:])
                list_email.insert(sn,str(sn-2)+'. '+a[1][8:])
                list_feedback.insert(sn,str(sn-2)+'. '+a[-1])
                #print('Date: ',t)
                #print('Subject: ',raw['Subject'])
                #print(s)

                #print('-------------------')



            

            Label(f,text='DATA TABLE',fg='orange',bg='white',font=('Times',20,'bold')).grid(row=1,column=3)
            Label(f,text='Enter the S.N. of the feedback\n you want to view :',font=('Times',12,'bold'),bg='white').place(anchor=CENTER,relx=0.84,rely=0.2)

            fno=Entry(f,bg='white',relief=SUNKEN,width=10)
            fno.place(anchor=CENTER,relx=0.84,rely=0.25)
            
    
            def view_feedback():
                if(fno.get()==''):
                    p1=Tk()
                    Label(p1,text='Enter Serial Number !',fg='red',bg='white').pack()
                    Button(p1,text="OK",command=p1.destroy).pack()
                    p1.configure(background='white')
                    p1.mainloop()
                elif(int(fno.get())<1 or int(fno.get())>len(msg_array)):
                    p2=Tk()
                    Label(p2,text='Invalid Serial Number !',fg='red',bg='white').pack()
                    Button(p2,text="OK",command=p2.destroy).pack()
                    p2.configure(background='white')
                    p2.mainloop()
                else:
                    feedback_msg=Tk()
                    Label(feedback_msg,text=msg_array[int(fno.get())-1],bg='white',relief='groove',wraplength=300,font=('Times',13)).pack(side=TOP)
                    Button(feedback_msg,text='Close',fg='white',bg='black',font=('Times',10),command=feedback_msg.destroy).pack(side=BOTTOM)
                    feedback_msg.configure(background='white')
                    feedback_msg.mainloop()
            
            Button(f,text='View Feedback',fg='black',bg='white',command=view_feedback).place(anchor=CENTER,relx=0.84,rely=0.3)   



            Button(f,text='Quit Window',fg='white',bg='red',font=('Times',14),command=f.destroy).place(anchor=CENTER,relx=0.52,rely=0.8)
            
              
            list_date.grid(row=2,column=1) 
            list_subject.grid(row=2,column=2)
            list_name.grid(row=2,column=3)
            list_email.grid(row=2,column=4)
            list_feedback.grid(row=2,column=5)
            f.configure(background='white')
            f.geometry('1500x1500')
            f.mainloop()

            


            
        
        Button(portal,text='View Queries',fg='white',bg='blue',font=('Times',20,'bold'),relief='raised',command=qwindow).place(anchor=CENTER,relx=0.47,rely=0.5)
        Button(portal,text='View Feedbacks',fg='white',bg='blue',font=('Times',20,'bold'),relief='raised',command=fwindow).place(anchor=CENTER,relx=0.47,rely=0.6)
        
        Button(portal,text='Quit',fg='white',bg='red',font=('Times',14,'bold'),relief='raised',command=portal.destroy).place(anchor=CENTER,relx=0.89,rely=0.9)

        portal.configure(background='white')
        portal.geometry('1500x1500')
        portal.mainloop()
    elif (e1.get()=='' or e1.get==' ') and (e2.get()=='' or e2.get==' '):
        temp=Tk()
        temp.title('Prompt')
        temp.configure(background='white')
        Label(temp,text='Enter data!',bg='white').pack()
        Button(temp,text='OK',command=temp.destroy).pack()
        temp.mainloop()
    else:
        e1.delete(0,END)
        e2.delete(0,END)
        warn=Tk()
        warn.title('Prompt')
        Label(warn,text='Wrong Data Entered!\nTry Again.',bg='white').pack()
        Button(warn,text='OK',command=warn.destroy).pack()
        warn.configure(background='white')
        warn.mainloop()
        


def quitroot():
    qroot=Tk()
    qroot.configure(background='white')
    Label(qroot,text='Are You Sure You Want To Exit ?',fg='red',bg='white',font=('Times',12,'bold')).pack(side=TOP)
    Button(qroot,text='NO',fg='blue',bg='white',command=qroot.destroy).pack(side=BOTTOM)
    def destroyall():
        qroot.destroy()
        root.destroy()
    Button(qroot,text='YES',fg='blue',bg='white',command=destroyall).pack(side=BOTTOM)
    qroot.mainloop()
    

b1=Button(root,text='LOGIN',font=('MS Sans serif',11,'bold'),fg='navy blue',bg='white',command=get_input,relief=RAISED).place(relx=0.48,rely=0.555,anchor=CENTER)

b2=Button(root,text='Exit',font=('verdana',11,'bold'),fg='red',bg='white',command=quitroot).place(relx=0.48,rely=0.68,anchor=CENTER)

root.geometry('1500x1500')
root.configure(background='white')
root.mainloop()
