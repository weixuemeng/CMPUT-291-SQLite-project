import sqlite3
import hashlib
import os.path
from operator import itemgetter
from datetime import date
import random
import tkinter as tkinter
from tkinter import Label,messagebox

def main():
    global cursor,connection,current_session, path
    try:
        if not path:
            connection = sqlite3.connect(path)
    except:
        path = database_path()
        connection = sqlite3.connect(path)
    cursor = connection.cursor()
    current_session = None
    start_GUI()

def database_path():
    path = input("Enter the path of the database: ")
    while(os.path.isfile(path) == False):
        path = input("Plase enter vaild path or name of the database: ")
    return path

def start_GUI():
    global window
    window = tkinter.Tk()
    window.title('Login system')
    window.geometry('400x180')
    window.resizable(width=True, height=True)
    user_lable = Label(window, text='User ID: ', font=('Helvetica', 15, 'bold'))
    user_lable.place(x=25, y=8)
    user_Entry = tkinter.Entry(window)
    user_Entry.focus_set()
    user_Entry.place(x=110, y=8)
    passwd_lable = Label(window, text='Password: ',font=('Helvetica', 15, 'bold'))
    passwd_lable.place(x=25, y=38)
    passwd_Entry = tkinter.Entry(window,show="*")
    passwd_Entry.focus_set()
    passwd_Entry.place(x=110, y=38)
    button = tkinter.Button(window, text='Login', width=9,font=('Helvetica', 13, 'bold'), command = lambda: login_check(user_Entry.get(),passwd_Entry.get()))
    button.place(x=270, y=70)
    button = tkinter.Button(window, text='Create user', width=9,font=('Helvetica', 13, 'bold'), command = lambda: Create_user())
    button.place(x=270, y=105)
    window.mainloop()


def hash_value(pwd):
    hashed_pwd = hashlib.sha1(str(pwd).encode('utf-8'))
    return hashed_pwd.hexdigest()

def existing_account():
    cursor.execute("SELECT U.uid FROM users U")
    uid = cursor.fetchall()
    uid = [i[0] for i in uid]
    users_id_pwd={}

    for i in uid:
        match_upwd = "SELECT U.pwd FROM users U WHERE U.uid = '{}'".format(i)
        cursor.execute(match_upwd)
        upwd = cursor.fetchall()
        upwd = [i[0] for i in upwd]
        hasd_upwd = hash_value(upwd[0])
        users_id_pwd[i.upper()] = hasd_upwd

    cursor.execute("SELECT A.aid FROM artists A")
    aid = cursor.fetchall()
    aid = [i[0] for i in aid]
    artists_id_pwd={}
    for i in aid:
        match_apwd="SELECT A.pwd FROM artists A WHERE A.aid = '{}'".format(i)
        cursor.execute(match_apwd)
        apwd = cursor.fetchall()
        apwd = [i[0] for i in apwd]
        hasd_apwd = hash_value(apwd[0])
        artists_id_pwd[i.upper()] = hasd_apwd
    return users_id_pwd, artists_id_pwd
        
def Create_user():
    user_act,_ = existing_account()
    while (1):
        print("==============================================")
        new_user_act = input("Please enter an account number that you want: "+'\n')
        if len(new_user_act) >4:
            print("===================================================")
            print("Sorry the account number must no more than 4 string ! ")
            print("===================================================")
            while(1):
                require = input("if you want to continue create user enter 1, else enter 2 to close the create system : ")
                if require == '2':
                    messagebox.showwarning(message="Create system closed, please back to login interface")
                    return -1
                if require == '1':
                    break
                else:
                    print("=================================")
                    print("Invalid input, Please Try again.")
                    print("=================================")
            continue
        elif new_user_act in user_act.keys():
            print("=======================================")
            print("Sorry the account number is occupied ! ")
            print("=======================================")
            while(1):
                require = input("if you want to continue create user enter 1, else enter 2 to close the create system : ")
                if require == '2':
                    messagebox.showwarning(message="Create system shutdown, please back to login interface")
                    return -1
                if require == '1':
                    break
                else:
                    print("=================================")
                    print("Invalid input, Please Try again.")
                    print("=================================")
            continue
        new_user_name = input("Please enter you name: ")
        new_user_pwd = input("Please enter an password that you want: ")
        if new_user_act not in user_act.keys() and len(new_user_act) <=4:
            anw = messagebox.askquestion(title='question', message='Do you want to create this account'+'\n'+'User ID: '+new_user_act+" ,User Name: "+new_user_name)
            print(anw)
            if anw == 'no':
                continue
            if anw == 'yes':
                print("==================================")
                print("The User is successfully created !")
                print("==================================")
                print("User ID: "+new_user_act+" User Name: "+new_user_name+" PASSWORD: "+new_user_pwd)
                print("=======================================================")
                print("Create system shutdown, please back to login interface ")
                print("=======================================================")
                cursor.execute("INSERT INTO users (uid,name,pwd) VALUES (?,?,?)", (new_user_act,new_user_name,new_user_pwd))
                connection.commit()
                return -1

def login_check(self_acnt, self_pwd):

    self_acnt=self_acnt.upper()

    user_act,artists_act=existing_account()

    if self_pwd != '':
        self_pwd = hash_value(self_pwd)
    if self_acnt in user_act.keys() and self_acnt in artists_act.keys():
        if self_acnt in user_act.keys() and user_act[self_acnt] == self_pwd and self_acnt in artists_act.keys() and artists_act[self_acnt] == self_pwd:
            messagebox.showwarning(title='Mutiple account exist',message=self_acnt+" is existing in both artist and user, please choose the one that you want to go")
            while(1):
                print("1. Enter 1 in order to login to user ")
                print("2. Enter 2 in order to login to artist ")
                select = input("Plase select the accont that you want to login: ")
                if select == '1':
                    cursor.execute("SELECT U.name,U.uid FROM users U WHERE UPPER(U.uid)= '%s'" %self_acnt )
                    users_name=cursor.fetchall()
                    current_login =users_name[0][0]
                    current_login_id =users_name[0][1]
                    print("============================")
                    print("You are in user mode !")
                    print(current_login+" is Online "+current_login_id)
                    print("============================")
                    user_select(current_login_id)
                if select == '2':
                    cursor.execute("SELECT A.name, A.aid FROM artists A WHERE UPPER(A.aid)= '%s'" %self_acnt )
                    artist_name=cursor.fetchall()
                    current_login =artist_name[0][0]
                    current_login_id =artist_name[0][1]
                    print("=============================")
                    print("You are in artist mode !")
                    print(current_login+" is Online " +current_login_id)
                    print("=============================")
                    artists_select(current_login_id)
                else:
                    print("===========================================")
                    print("ERROR : invalid input ! Please enter 1 or 2")
                    print("===========================================")
        elif user_act[self_acnt] == self_pwd:
            cursor.execute("SELECT U.name, U.uid FROM users U WHERE UPPER(U.uid)= '%s'" %self_acnt )
            users_name=cursor.fetchall()
            current_login =users_name[0][0]
            current_login_id =users_name[0][1]
            messagebox.showinfo(title='successfully logged in',message="Hello "+current_login+",You have successfully logged in")
            print("============================")
            print("You are in user mode !")
            print(current_login+" is Online "+current_login_id)                
            print("============================")
            user_select(current_login_id)
        elif artists_act[self_acnt] == self_pwd:
            cursor.execute("SELECT A.name, A.aid FROM artists A WHERE UPPER(A.aid)= '%s'" %self_acnt )
            artist_name=cursor.fetchall()
            current_login =artist_name[0][0]
            current_login_id =artist_name[0][1]
            messagebox.showinfo(title='successfully logged in',message="Hello "+current_login+",You have successfully logged in")
            print("=============================")
            print("You are in artist mode !")
            print(current_login+" is Online "+current_login_id)
            print("=============================")
            artists_select(current_login_id)
        else:
            messagebox.showerror(message="Your password or username is incorrect, make sure your input is correct")
    else:
        if self_acnt in user_act.keys() and user_act[self_acnt] == self_pwd:
            cursor.execute("SELECT U.name, U.uid FROM users U WHERE UPPER(U.uid)= '%s'" %self_acnt )
            users_name=cursor.fetchall()
            current_login =users_name[0][0]
            current_login_id =users_name[0][1]
            messagebox.showinfo(title='successfully logged in',message="Hello "+current_login+",You have successfully logged in")
            print("============================")
            print("You are in user mode !")
            print(current_login+" is Online "+current_login_id)                
            print("============================")
            user_select(current_login_id)
        elif self_acnt in artists_act.keys() and artists_act[self_acnt] == self_pwd:
            cursor.execute("SELECT A.name, A.aid FROM artists A WHERE UPPER(A.aid)= '%s'" %self_acnt )
            artist_name=cursor.fetchall()
            current_login =artist_name[0][0]
            current_login_id =artist_name[0][1]
            messagebox.showinfo(title='successfully logged in',message="Hello "+current_login+",You have successfully logged in")
            print("=============================")
            print("You are in artist mode !")
            print(current_login+" is Online "+current_login_id)
            print("=============================")
            artists_select(current_login_id)
        else:
            messagebox.showerror(message="Your password or username is incorrect, make sure your input is correct")

def userquit(uid):
    global connection, cursor, current_session
    if current_session != None:
        has_sno  = cursor.execute('''SELECT * 
                                    FROM sessions
                                    WHERE uid =:uid AND sno=:sno
                        ''', {"uid":uid,"sno":current_session[1]}).fetchall()

        if len(has_sno)>0:
            #user has a session
            end = date.today()
            cursor.execute(''' UPDATE sessions
                            SET  end =:end
                            WHERE uid=:uid AND sno=:sno
                            ''',{"end":end, "uid":uid, "sno": current_session[1]})

        connection.commit()

    messagebox.showinfo(title='successfully logged out',message="Hello "+uid+",You have successfully logged out")
    window.destroy()
    main()

def quit(aid):
    messagebox.showinfo(title='successfully logged out',message="Hello "+aid+",You have successfully logged out")
    window.destroy()
    main()

def start_session(self_uid):
    global connection, cursor , current_session
    uni_sno = 0
    cursor.execute('''SELECT sno 
                      FROM sessions se
                      WHERE  se.uid =:uid''',{"uid":self_uid})
    exist_sno = [i[0] for i in cursor.fetchall()]
    if len(exist_sno)>0: 
        # exist sno
        uni_sno = max(exist_sno) +1
    else:
        # no exist sno : create new one
        uni_sno = random.randint(0,1000)

    start_date = date.today()
    end_date = None
    cursor.execute('''INSERT INTO sessions(uid,sno,start,end) VALUES (?, ?, ?,?)
                    ''', (self_uid, uni_sno,start_date, None))
    current_session = (self_uid, uni_sno)
    connection.commit()

    return uni_sno

def search_song_playlist(self_uid):
    global connection, cursor
    keywords = input("Please enter (a) keyword(s) to find songs and playlists: ")
    while len(keywords.strip())==0:
        keywords = input("Please enter (a) valid keyword(s) or type 'exit' to return to main menu: ")
    if keywords.strip() =="exit":
        return
    
    while(1):
        keywords = keywords.split() 
        songs_playlists_dict= {} # used to count how many keywords a song/playlist fit in
        for k in keywords:
            k_cap = "%{upper}%".format(upper = k.upper())
            cursor.execute('''SELECT 'Song',*
                            FROM songs s
                            WHERE upper(s.title) LIKE :k_cap
                            UNION
                            SELECT distinct 'Playlist', p.pid, p.title, IFNULL(sum(s.duration),0) as total_duration
                            FROM playlists p left join plinclude pl using (pid) 
                                left join songs s using (sid)
                            WHERE upper(p.title) LIKE :k_cap
                            GROUP BY p.pid, p.title
            ''',{"k_cap": k_cap})

            songs_playlists = cursor.fetchall()
            for p in songs_playlists:
                if p not in songs_playlists_dict.keys():
                    songs_playlists_dict[p] = 1
                else:
                    songs_playlists_dict[p]+=1

        # sorted the result  format: [ (("Playlist","pid1","title1","duration1"), 1 ),(("Playlist","pid2","title2","duration2"), 2 ) ]
        res_list = sorted(songs_playlists_dict.items(), key = itemgetter(1), reverse = True)

        # if >5 matching: show 5
        if len(res_list) >5:
            print("===============================================\n")
            print("Category"+ "id".rjust(5)+"title".rjust(20)+"duration".rjust(25)+'\n')
            for  i in range(0,5):
                print(res_list[i][0][0].ljust(8)+"  "+str(res_list[i][0][1]).ljust(10),res_list[i][0][2].ljust(30),res_list[i][0][3])
            print("===============================================\n")

            see_rest = input("Type (y/n) to see the rest of the result: ").lower()
            while see_rest not in ['y','n']:
                see_rest = input("Type (y/n) to see the rest of the result: ").lower()
            print("")
            if see_rest.strip()== 'y':
                for i in range(5,len(res_list)):
                    #show the rest
                    print(res_list[i][0][0].ljust(8)+"  "+str(res_list[i][0][1]).ljust(10),res_list[i][0][2].ljust(30),res_list[i][0][3])
        
        # if <5 matchingL show all
        else:
            # no matching
            if len(res_list)==0 : 
                print("There are no matching songs or playlists !!\n")
                return
            
            # has matching
            print("")
            print("===================================================================")
            print("Category"+ "id".rjust(4)+"title".rjust(20)+"duration".rjust(25)+'\n')
            for i in res_list:
                i = list(i)[0]
                print(i[0].ljust(8)+"  "+str(i[1]).ljust(10)+i[2].ljust(30)+" "+str(i[3]))
            print("===================================================================")
        # asked the user to select a song/playlist
        user_select = input("\nSelect the category (enter 'p or P' for playlist or enter 's' or 'S' for song) : ")
        while user_select.strip().lower() != "p"and user_select.strip().lower() != "s" :
            user_select = input("Please enter a valid category (playlist or songs): ")

        #check category
        if user_select.strip().lower() =="p" and valid_category_check("Playlist",songs_playlists_dict) == False:
            print("There is no playlist in the searching result ! \n")
            user_select = input("Please enter select a song('s' or 'S') or enter 'next' to see more options: ")
            while user_select not in ['s','S','next']:
                user_select = input("Please enter select a song('s' or 'S') or enter 'next' to see more options: ")
            if user_select=='next':
                break

        elif user_select.strip().lower() =="s" and valid_category_check("Song",songs_playlists_dict) == False:
            print("There is no song in the searching result !\n")
            user_select = input("Please enter select a song('p' or 'P') or enter 'next' to see more options: ")
            while user_select not in ['p','P','next']:
                user_select = input("Please enter select a song('p' or 'P') or enter 'next' to see more options: ")
            if user_select=='next':
                break

        # option 1: select playlist
        if user_select.strip().lower()== 'p':
            playlist_pid = input("\nEnter the id of the playlist: ")
            # error checking ( pid is valid)
            while(len(playlist_pid.strip())==0 or playlist_error_checking(int(playlist_pid), songs_playlists_dict)== False):
                playlist_pid = input("Can't find input id. Please enter a valid id: ")
                while playlist_pid.isdigit()==False:
                    playlist_pid = input("Please enter a valid id or playlist: ")
            
            playlist_pid= int(playlist_pid)
            s_in_playlist = cursor.execute('''  SELECT distinct s.sid, s.title, s.duration 
                                                FROM plinclude pl, songs s
                                                WHERE pl.sid = s.sid
                                                AND pl.pid = :playlist_pid
                                        ''', {"playlist_pid": playlist_pid}).fetchall()
            sid_in_playlist = [i[0] for i in s_in_playlist]
            if len(s_in_playlist)>0:
                # has record in selected playlist
                print("\n================================")
                print(" id     title     duration")
                for s in s_in_playlist:
                    print(" "+str(s[0]).ljust(4)+str(s[1]).ljust(20)+str(s[2]).rjust(6))
                print("==================================\n")

                print("================================================")
                print("|   Option              description            |")
                print("|      1              Back to main menu        |")
                print("|      2     select a song from this playlist  |")
                print("================================================\n")
  
                print("==============================================")
                keywords = input("Please select an option: ").strip()
                while keywords not in ["1","2"]:
                    keywords = input("Please select a valid option: ").strip()

                if keywords =="1":
                    break

                # song action
                print("==============================================")
                song_sid = input("Enter the id of the song: ")
                while song_sid.isdigit() == False or int(song_sid) not in sid_in_playlist :
                     song_sid = input("Please enter a valid id of the song: ")
                print("")
                song_action(self_uid, int(song_sid)) 

            else:
                #back to main menu
                print("\nThere is no song in this playlist ! \n") 
 
        else: # option 2: select song
            song_sid = input("Enter the id of the song: ").strip()
            while song_sid.isdigit()==False:
                song_sid = input("Please enter a valid id of the song: ")
               
            # error checking( uid is valid)
            while(song_error_checking(int(song_sid), songs_playlists_dict)== False):
                song_sid = input("Can't find input id. Please enter a valid id: ").strip()
                while song_sid.isdigit()==False:
                    song_sid = input("Please enter a valid id of the song: ")


            song_action(self_uid, int(song_sid))

        print("===============================================")
        print("|   Option              description           |")
        print("|      1               Back to main menu      |")
        print("|      2        new search songs and playlist |")
        print("===============================================")
        keywords = input("Please select an option: ").strip()
        print("")
        while keywords not in ["1","2"]:
            keywords = input("Please select a valid listed option from the table: ")

        if keywords =="1":
            break

        keywords = input("Please enter (a) keyword(s) to find songs and playlists: ")
        while len(keywords.strip())==0:
            keywords = input("Please enter (a) valid keyword(s) to find songs and playlists: ")

    connection.commit()
    return

def listen(self_uid,song_sid):
    '''
        a listening event is recorded within the current session of the 
        user((if a session has already started for the user) or within 
        a new session (if not))
    '''
    global connection, cursor,current_session

    if current_session==None:
        start_session(self_uid)

    listen_record = cursor.execute('''  SELECT * 
                                        FROM listen l
                                        WHERE l.uid = :uid AND l.sno = :sno AND l.sid=:sid
                                    ''', {"uid": self_uid,"sno":current_session[1],"sid":song_sid}).fetchall()
    if len(listen_record) ==0:
        cursor.execute('''INSERT INTO listen(uid,sno,sid,cnt) VALUES
                            (?,?,?,?)
                        ''', (self_uid,current_session[1],song_sid,1))
    else:
        cursor.execute('''UPDATE listen
                            SET cnt = cnt+1
                            WHERE uid = :uid AND sno = :sno AND sid = :sid
                        ''', {"uid":self_uid, "sno": current_session[1],"sid": song_sid})

    connection.commit()
    return 

def song_action(self_uid, song_sid):
    print("=========================================")
    print("|  Option  |         Description        |")
    print("=========================================")
    print("|    1     |     Listen to this song    |\n")
    print("|    2     |    See more information    |\n")
    print("|    3     |      Add into playlist     |")
    print("=========================================\n")

            # action on selected song
    option = input("\nPlease select one option from the menu: ").strip()
    while(option not in ["1","2","3"]):
        option= input("invalid option. Please enter it again: ")
            
    if option == "1": # listen to this song
        print("Listen ...\n")
        listen(self_uid, song_sid)
    if option == "2": # see more information
        see_information(song_sid)
    if option =="3": # add into playlist
        add_to_playlist(self_uid, song_sid)

def see_information(song_sid):
    '''
    More information for a song is the names of artists who performed 
    it in addition to id, title and duration of the song as well as 
    the names of playlists the song is in (if any).
    '''
    global connection, cursor
    # need LEFT JOIN on Playlists
    information= cursor.execute(''' SELECT DISTINCT  s.sid, s.title,  a.name, s.duration, IFNULL(p.title,"No playlist match")
                                    FROM songs s LEFT JOIN plinclude pl USING (sid) LEFT JOIN playlists p USING(pid), perform per, artists a
                                    WHERE s.sid = per.sid AND per.aid = a.aid
                                          AND s.sid =:sid
                                    GROUP BY s.sid, s.title, s.duration, p.title;
                                ''', {"sid":song_sid})
    print("\nGet information...\n")
    print("==============================================================================================================")
    #print(" id      title     artist(s)      duration      playlists      ")
    for info in information:
        print(" SID: %s     title: %s     artist(s): %s     duration: %s     playlists: %s"%(info[0],info[1],info[2],info[3], info[4]))
    print("==============================================================================================================")
    print("")
    connection.commit()

    return

def add_to_playlist(self_uid, song_sid):
    '''
    When adding a song to a playlist, the song can be added to an 
    existing playlist owned by the user (if any) or to a new playlist.

    When it is added to a new playlist, a new playlist should be
    created with a unique id (created by your system) and the uid set
    to the id of the user and a title should be obtained from input. 
    
    '''
    global connection, cursor
    cursor.execute(''' SELECT pid,title
                       FROM playlists p
                       WHERE uid = :uid
                    ''', {"uid":self_uid})
    user_playlist = [i for i in cursor.fetchall()]
    user_pid = [i[0] for i in user_playlist]
    uni_pid = None

    if len(user_playlist)==0: # the user has no playlist ( add to new playlist)
        # system assign new pid
        cursor.execute('''SELECT pid
                          FROM playlists p
                        ''')
        exist_pid = [i[0] for i in cursor.fetchall()]
        if len(exist_pid)>0:
            #exist playlist 
            uni_pid = max(exist_pid)+1
        else:
            # no exit playlist
            uni_pid = random.randint(0,1000)
        
        playlist_title = input("\nPlease enter your playlist name: ").strip()
        while len(playlist_title)==0 :
            playlist_title = input("\nPlease enter a valid playlist name: ").strip()

        # update playlist table
        cursor.execute('''INSERT INTO playlists VALUES
                        (:pid, :title, :uid)
                        ''', {"pid":uni_pid,"title":playlist_title,"uid":self_uid})
        # update plinclude table
        cursor.execute('''INSERT INTO plinclude(pid,sid,sorder) VALUES (?,?,?) 
                           ''', (uni_pid, song_sid, 1))

    else:# user has exist playlists
        print("===========================")
        print("playlist_id    title    \n")
        for i in user_playlist:
            print(str(i[0]).ljust(4)+" "+i[1])
        print("===========================\n")
        
        new_pid = str(input("Do you want to create a new playlist? (please enter 'y' for yes or 'n' for no: ").strip().lower())
        if new_pid not in ["y", "n"]:
            new_pid = str(input("please enter a valid option: 'y' for yes or 'n' for no: ").strip())
        
        if new_pid == "y":
            # user want to create a new playlist ( he cannot find a playlist he want to add to)
            cursor.execute('''SELECT pid
                          FROM playlists p
                        ''')
            exist_pid = [i[0] for i in cursor.fetchall()]
            uni_pid = max(exist_pid)+1

            playlist_title = input("\nPlease enter your playlist name: ").strip()
            while len(playlist_title)==0 :
                playlist_title = input("\nPlease enter a valid playlist name: ").strip()

            # update playlist table
            cursor.execute('''INSERT INTO playlists VALUES
                            (:pid, :title, :uid)
                            ''', {"pid":uni_pid,"title":playlist_title,"uid":self_uid})
            # update plinclude table          
            cursor.execute('''INSERT INTO plinclude(pid,sid,sorder) VALUES (?,?,?) 
                            ''', (uni_pid, song_sid, 1))
        
        else:
            to_pid = input("\n Please select the playlist id where you want to put the song: ").strip()
            while to_pid.isdigit() == False:
                to_pid = input("\n Please select a valid playlist id where you want to put the song: ").strip()


            while int(to_pid) not in user_pid:
                to_pid = input("\n Invalid id, Please check again and enter the playlist id where you want to put the song: ").strip()
                while to_pid.isdigit() == False:
                    to_pid = input("\n Please select a valid playlist id where you want to put the song: ").strip()
            
            to_pid = int(to_pid)
            # find current order
            current_order = cursor.execute('''SELECT MAX(sorder)
                            FROM plinclude 
                            WHERE pid = :pid''',{"pid": to_pid}).fetchone()[0]
            # check if the song is already in the playlist the user selected
            song_in_p = cursor.execute(''' SELECT sid
                                        FROM plinclude
                                        WHERE pid = :pid''', {"pid":to_pid}).fetchall()
            songs_in_p = [i[0] for i in song_in_p]
            print(songs_in_p)
            print("song_id",song_sid)
            if song_sid in songs_in_p:
                print("Your selected song is already in your selected playlist\n")
            else: # if selected is not in the playlist
                cursor.execute('''INSERT INTO plinclude(pid,sid,sorder) VALUES (?,?,?) 
                            ''', (to_pid, song_sid, current_order+1))
    connection.commit()
    return 

def valid_category_check(category,song_playlist_dict ):
    for record in song_playlist_dict:
        if record[0]== category:
            return True
    return False

def song_error_checking(sid, song_playlist_dict):
    find = False
    for i in song_playlist_dict:
        if i[0]=="Song":
            if i[1] == sid:
                return True
    return False

def playlist_error_checking(pid, song_playlist_dict):
    find = False
    for i in song_playlist_dict:
        if i[0]=="Playlist":
            if i[1] == pid:
                return True
    return False

def user_select(self_uid):

    print("=============================================")
    print("|                    MENU                   |")
    print("---------------------------------------------")
    print("|  Option  |            Description         |")
    print("=============================================")
    print("|    1     |         Start a session        |\n")
    print("|    2     | Search for songs and playlists |\n")
    print("|    3     |        Search for artists      |\n")
    print("|    4     |        End the session         |")
    print("=============================================\n")
    option = input("\nPlease select one option: ").strip()
    while option not in ["1","2","3","4"]:
        option = input("\nPlease select one option: ").strip()
    option = int(option)
    while( option!= 4):
        if option == 1:
            if( current_session != None):
                print("You already in a session ! ")
            else:
                sno = start_session(self_uid)
                name = cursor.execute('''SELECT name 
                                        FROM users
                                        WHERE uid =:uid''', {"uid":self_uid}).fetchone()[0]
                print("Welcome {name} to Session {sno} ".format(name = name, sno =sno ))
        elif option==2:
            search_song_playlist(self_uid)
        elif option==3:
            search_artist(self_uid)

        print("=============================================")
        print("|                    MENU                   |")
        print("============================================\n")
        print("|  Option  |            Description         |\n")
        print("|    1     |         Start a session        |\n")
        print("|    2     | Search for songs and playlists |\n")
        print("|    3     |        Search for artists      |\n")
        print("|    4     |        End the session         |\n")
        print("=============================================\n")
        
        option = input("\nPlease select one option: ").strip()
        while option not in ["1","2","3","4"]:
            option = input("\nPlease select one option: ").strip()
        option = int(option)
    userquit(self_uid)

def search_artist(self_uid):
    """
    This part is only for "Search for artists",The system temporarily supports asking the user to enter 
    multiple keywords,  the The system will automatically match the keywords, note that keywords is a 
    completed word, so the system will only match all the names and songs by dividing them into many
    words through spaces. When the matching is done, the system will sort by the number of times you 
    enter the keywords, and output artist, Nationality, and the total number of 
    songs they have in the perform in the database.

    ALL the data is insert already please do not do it again

    """
    print(self_uid+' is start searching')
    cursor.execute("""SELECT tb1.name, tb1.nationality, IFNULL(S.title,'')
                        FROM (select A.name, A.nationality, P.sid
                        from artists A
                        left Join perform P
                        ON A.aid = P.aid) as tb1
                        left join songs S
                        On tb1.sid = S.sid
                         """)
    combine = cursor.fetchall()
    combine = [i for i in combine]

    matched=[]
    Key_list=[]

    while(1):
        print("===========================================================================================")
        keywords = str(input("Please enter 'exit' to end, or enter the keywords that you wannt to search: "))
        if keywords =='exit':
            break
        elif keywords !='':
            keyword=[]
            keyword = keywords.split()
            if len(keyword)>1:
                Key_list.extend(keyword)
            else:
                Key_list.append(keywords.strip())

    if len(Key_list) ==0:
        print("===============================================")
        print("|   ERROR:    No keywords was been enter      |")
        print("|      1             Back to main menu        |")
        print("|      2      Enter any key back to main menu |")
        print("===============================================")
        exit = str(input("Please enter 1 to start the keyword(s) search again, or enter any words to back to main menu "))
        if exit == "1":
            search_artist(self_uid)
        else:
            return      

    check1 = []
    check2 = []
    count =0

    for key in Key_list:
        for i in combine:
            Aelement_up=[Aelem.upper()for Aelem in i[0].split()]
           # print(Aelement_up)
            Selement_up=[Selem.upper()for Selem in i[2].split()]
            #print(Selement_up)
            for j in Aelement_up:
                if key.upper() in j:
                    if key+i[0] in check1:
                        continue
                    else:
                        print("=================================================")
                        print("By Keywords: '"+key+"' system matched artist: "+i[0])
                        matched.append(i[0])
                        count+=1
                        check1.append(key+i[0])

            for f in Selement_up:
                if key.upper() in f:
                    if key+i[2] in check2:
                        continue
                    else:
                        print("=================================================")
                        print("By Keywords: '"+key+"' system matched song: "+i[2])
                        for j in combine:
                            if j[2]==i[2]:
                                print("song is made by: "+j[0])
                                matched.append(j[0])
                        count+=1
                        check2.append(key+i[2])
        if count == 0:
            print("=================================================")
            print("By Keywords: '"+key+"' system did not find any match song or artist" )
        count =0

    if len(matched) ==0:
        print("===============================================")
        print("|   ERROR:  No matched find by your keyword(s)|")
        print("|      1        Start a new artist search     |")
        print("|      2      Enter any key back to main menu |")
        print("===============================================")
        exit = str(input("Please enter 1 to start the keyword(s) search again, or enter any words to back to main menu: "))
        if exit == "1":
            search_artist(self_uid)
        else:
            return

    print("=================================================\n")
    match_count=[]
    for i in matched:
        sub_count=(i, matched.count(i))
        match_count.append(sub_count)
    match_count=list(dict.fromkeys(match_count))
    combine_list=[]
    for i in match_count:
        for j in combine:
            if i[0] == j[0]:
                count=0
                for z in combine:
                    if z[0]==j[0] and z[2]!='':
                        count+=1
                sub_list=(i[0],j[1],count,i[1])
                combine_list.append(sub_list)
                combine_list=list(dict.fromkeys(combine_list))
    combine_list.sort(key=sort_key, reverse=True)
    select_artist=cheking(combine_list)

    cursor.execute(""" select s.sid,s.title,s.duration
                    from songs s, perform p, artists a
                    where s.sid=p.sid and a.aid=p.aid and A.name = :name""",{"name":select_artist})
    artist_songs = cursor.fetchall()
    artist_songs = [i for i in artist_songs]

    if len(artist_songs) ==0:
        print("===============================================")
        print("|      No song is perform by this artsit      |")
        print("|      1        Start a new artist search     |")
        print("|      2      Enter any key back to main menu |")
        print("===============================================")
        exit2 = str(input("Please enter 1 to start the keyword(s) search again, or enter any words to back to main menu "))
        if exit2 == "1":
            search_artist(self_uid)
        else:
            return

    print("===========================================================================================")
    print('You have selected : ',select_artist,' The songs created by this artist are: ')

    for i in range(0,len(artist_songs)):
        print(i+1," SID: "+str(artist_songs[i][0]).ljust(15)+" Song Title: "+artist_songs[i][1].ljust(15)+" Song Duration: ",artist_songs[i][2])
    while(1):
        print("")
        select_song= input("Please select one song that you want to operate by the number at first col: ")
        if select_song.isdigit() and int(select_song) < len(artist_songs)+1:
            current_song = artist_songs[int(select_song)-1]
            print("===========================================================================================")
            print("You selected song : "+str(current_song[1])+" Sid for this song is: "+str(current_song[0]))
            break
        else:
            print("=================")
            print("Invalid input")
    song_action(self_uid, current_song[0])
    print("===============================================")
    print("|    info:      current artsit search end     |")
    print("|      1        Start a new artist search     |")
    print("|      2      Enter any key back to main menu |")
    print("===============================================")
    exit3 = str(input("Please enter 1 to start the keyword(s) search again, or enter any words to back to main menu "))
    if exit3 == "1":
        search_artist(self_uid)
    else:
        return
    
def cheking(combine_list):
    dis_count=0
    iteration=0
    for i in range(0,len(combine_list)):
        dis_count+=1
        print(i+1," Artist: "+combine_list[i][0].ljust(15)+" Nationality: "+combine_list[i][1].ljust(15)+" Number of performed songs: ",combine_list[i][2])
        if dis_count >4 and len(combine_list)-iteration-dis_count !=0:
            while(1):
                print("===========================================================================================")
                user_s = input("type '.next' to check next page, or select the artist by the number at first col :")
                if user_s == '.next':
                    iteration+=5
                    dis_count=0
                    break
                elif user_s.isdigit() and int(user_s)<=int(iteration)+dis_count and int(user_s) !=0:
                    select_artist = combine_list[int(user_s)-1][0]
                    return select_artist
                else:
                    print("=================")
                    print("Invalid out put")
        elif dis_count == len(combine_list) or dis_count ==len(combine_list)-int(iteration):
            while(1):
                print("========================================================================================")
                select = input("Please select the artist by the number at first col : ")
                if select.isdigit() and int(select)<=len(combine_list) and int(select) !=0:
                    select_artist=combine_list[int(select)-1][0]
                    return select_artist
                else:
                    print("=================")
                    print("Invalid out put")

def sort_key(list):
    return list[3]

def artists_select(self_uid):

    print("=============================================\n")
    print("|                    MENU                   |\n")
    print("=============================================\n")
    print("|  Option  |            Description         |\n")
    print("|    1     |         Add a new song         |\n")
    print("|    2     | Find top 3 users and playlists |\n")
    print("|    3     |             EXIST              |\n")
    print("=============================================\n")
    option = input("\nPlease select one option: ").strip()
    while option not in ["1","2","3"]:
        option = input("\nPlease select one option: ").strip()

    while( option!= "3"):
        if option == "1":
            artists_insertsong(self_uid)
        elif option== "2":
            findtp_l(self_uid)
        print("=============================================\n")
        print("|                    MENU                   |\n")
        print("=============================================\n")
        print("|  Option  |            Description         |\n")
        print("|    1     |         Add a new song         |\n")
        print("|    2     | Find top 3 users and playlists |\n")
        print("|    3     |             EXIST              |\n")
        print("=============================================\n")
        option = input("\nPlease select one option: ").strip()
        while option not in ["1","2","3"]:
            option = input("\nPlease select one option: ").strip()
    quit(self_uid)

def artists_insertsong (self_uid):
    n_title = str(input("Please enter the title of the song you want to insert: "))
    while len(n_title)==0:
        n_title = str(input("Please enter the valid title of the song: "))

    n_duration= str(input("Please enter the duration of the song you want to insert: "))

    while(1): #make sure the duration is number    
        if n_duration.isdigit():
            break        
        else:
            n_duration= str(input("Invalid input! Please enter the duration of the song again: "))

    s_duration = int(n_duration)

    cursor.execute("SELECT S.duration FROM songs S, perform P, artists A WHERE S.sid = P.sid and P.aid = A.aid and lower(A.aid) = ? and lower(S.title) = ?",(self_uid.lower(),n_title.lower()))
    check_songs = cursor.fetchall()#include all the songs pefromed by the user and the title equal to the input
    check_songs = [i[0] for i in check_songs]


    if s_duration in check_songs:#the song has same duration and same title
        print("Deny insertion!This song already existed.")
    else:
        cursor.execute("SELECT S.sid FROM songs S")
        sid = cursor.fetchall()
        sid = [i[0] for i in sid]
        uni_sid = None
        if( len(sid) >0):  #change
            uni_sid = max(sid)+1
        else:
            uni_sid = random.randint(0,1000)#create the unique sid for the song

        aid_perform=[]
        ask1 = input("if this song is create by multiple artists enter 2, if not enter 1: ").strip()
        while ask1 not in ["1","2"]:
            print("\nPlease enter a valid option")
            ask1 = input("if this song is create by multiple artists enter 2, if not enter 1: ").strip()

        while(1): # change 
            while ask1 not in ["1","2"]:
                print("\nPlease enter a valid option")#avoid program crush if user enter the wrong value
                ask1 = input("if this song is create by multiple artists enter 2, if not enter 1: ").strip()
            
            if ask1 == "1": # no artist perform together
                break
            elif ask1 == "2": # other artists perform together
                ask2=input("enter the cooporate artist id: ").strip()
                cursor.execute("SELECT DISTINCT A.aid FROM artists A")
                aid = cursor.fetchall()
                aid = [i[0] for i in aid] #added
                while(1):    
                    if ask2 in aid and ask2 not in aid_perform and ask2!=self_uid:
                        aid_perform.append(ask2)
                        ask1 = input("if this song is create by other multiple artists enter 2, if not enter 1: ").strip()
                        break
                    else:
                        ask2=input("The artist does not exist or the artists already has inserted,please enter cooporate artist id again: ").strip()
        aid_perform.append(self_uid)
        
        # add song into song table
        add_s= "INSERT INTO songs (sid,title,duration) VALUES(?,?,?);"
        cursor.execute(add_s,(uni_sid,n_title, s_duration))

        print("Song added successfully !")
        connection.commit()
        
        # add artist if and song id into perform table
        for i in aid_perform:
            add_p = "INSERT INTO perform (sid,aid) VALUES(?,?);" 
            cursor.execute(add_p,(uni_sid,i))
            connection.commit()

def findtp_l(self_uid):
    print("=============================================")
    print("|                    MENU                   |")
    print("=============================================")
    print("|  Option  |            Description         |\n")
    print("|    1     |         Find top 3 users       |\n")
    print("|    2     |       Find top 3 playlists     |\n")
    print("|    3     |             EXIST              |")
    print("=============================================\n")

    ask3 = input("Please select one option: ")
    while(1):
        if ask3 == "1":
            cursor.execute('''SELECT DISTINCT l.uid , u.name
                        From listen l,songs s,perform p, users u
                        Where l.sid= s.sid and s.sid=p.sid and u.uid = l.uid and lower(p.aid) = ?
                        group by l.uid
                        ORDER BY sum(l.cnt*s.duration)DESC
                        LIMIT 3;''',(self_uid.lower(),))
            top_fans= cursor.fetchall()
            print("Finding top users: ")
            for fan in top_fans:
                print("uid: "+fan[0]+"  name: "+fan[1])
            break
        
        elif ask3 == "2":
            cursor.execute('''select pi1.pid, ps.title
                            from plinclude pi1, perform p1, playlists ps
                            where  pi1.sid = p1.sid and pi1.pid = ps.pid and lower(p1.aid) = ?
                            group by pi1.pid
                            order by count(p1.sid) desc
                            limit 3;''',(self_uid.lower(),))
            top_lists= cursor.fetchall()
            print("Finding top Playlists: ")
            for pl in top_lists:
                print("playlist id: "+str(pl[0]))
                print("playlist title: "+str(pl[1]))
                print("")
            break

        elif ask3 == "3":
            break

        else:
            ask3=input("Invalid input!Please enter it again: ") 
if __name__ == "__main__":
    
    main()

