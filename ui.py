#Experimental class for the ui
class ui(object):
    """
    The ui class
    """
    def __init__(self):
        self.fulscreen = False
        self.extension = False
        self.pms = []
        self.pm_index = 0
        #Try to connect to the database server
        if args["backend"] is not None:
            pm = sqltoplib.create_connection(backend=args["backend"], host=args["host"], user=args["user"], password=args["password"], port=args["port"])
            try:
                pm.connect()
            except sqltoplib.processmanager.ProcessManagerError:
                pass
        else:
            pm = sqltoplib.create_connection(backend="dummy")
        (max_y, max_x) = scr.getmaxyx()
        try:
             curses.use_default_colors()
        except curses.error:
             pass
        self.scr.nodelay(1)
        self.scr.keypad(1)
        self.maxInfo = (max_x-75)
        self.delay_counter = 1
        self.delay = 1
        self.paused = False
        self.history = False
        self.history_pos = 0
        self.cursor_pos = 0
        self.cursor_max_pos = 0
        self.pm_index = 0
        self.pms = []
        self.pms.append(pm)
        self.fullscreen = args["fullscreen"]
        self.extension = False
        
    def start_ui():
        print "todo"
        
    def write_to_file(scr, pm, fullscreen=False):
        """
        Write process to file in a csv format
        """
        scr.addstr(3, 0, 'Write to : ')
        scr.move(3, 11)
        scr.nodelay(0)
        curses.echo()
        scr.refresh()
        path = scr.getstr()
        if os.path.exists(path) & os.path.isfile(path):
            scr.move(3, 0)
            scr.clrtoeol()
            curses.noecho()
            curses.curs_set(0)
            scr.addstr(3, 0, 'File exist. Do you want to overwrite ? [y/N]')
            resp = scr.getch()
            if resp == ord("y"):
                scr.refresh()
                try :
                    output_file = open(path, "w")
                    output_file.write("Id;User;Host;Db;State;Time;Info\n")
                    for process in pm.process:
                        line = str(process.pid) + ";" + process.user + ";" + process.host + ";" + process.db + ";" + process.state + ";" + str(process.time) + ";" + process.info
                        output_file.write(line + "\n")
                    output_file.close()
                except IOError:
                    scr.move(3, 0)
                    scr.clrtoeol()
                    scr.addstr(3, 0, 'Impossible to write file')
                    scr.refresh()
                    time.sleep(1)
        else:
            try :
                output_file = open(path, "w")
                output_file.write("Id;User;Host;Db;State;Time;Info\n")
                for process in pm.process:
                    line = str(process.pid) + ";" + process.user + ";" + process.host + ";" + process.db + ";" + process.state + ";" + str(process.time) + ";" + process.info
                    output_file.write(line + "\n")
                output_file.close()
            except IOError:
                scr.move(3, 0)
                scr.clrtoeol()
                scr.addstr(3, 0, 'Impossible to write file')
                scr.refresh()
                time.sleep(1)
        curses.noecho()
        curses.curs_set(1)
        scr.nodelay(1)
        scr.refresh()

    def change_delay(scr, fullscreen=False):
        (max_y, max_x) = scr.getmaxyx()
        if fullscreen:
            ques_pos = max_y - 1
        else:
            ques_pos = 3
        scr.addstr(ques_pos, 0, 'Specify delay in second : ')
        scr.nodelay(0)
        curses.echo()
        scr.refresh()
        try:
            delay = int(scr.getstr())
        except ValueError:
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, 'Bad delay value')
            scr.refresh()
            time.sleep(1)
            delay = None
        curses.noecho()
        scr.nodelay(1)
        scr.refresh()
        scr.erase()
        return delay

    def ask(scr, fullscreen=False):
        (max_y, max_x) = scr.getmaxyx()
        if fullscreen:
             ques_pos = max_y - 1
        else:
             ques_pos = 3
        scr.nodelay(0)
        curses.echo()
        scr.move(ques_pos, 0)
        scr.clrtoeol()
        scr.addstr(ques_pos, 0, "command : ")
        command = scr.getstr()
        if command == "backend":
            response = "List of disponible backend\n\n"
            for backend in sqltoplib.DISPONIBLE_BACKEND:
                response = response + backend + "\n"
        elif command == "help":
            response = """ List of disponible command\n\n
     backend   List disponible backend
     load      Load connection
     save      save current connection
     help      Display this help
     quit      Quit
    """
            
        elif command == "quit":
            sys.exit(0)
        scr.erase()
        scr.nodelay(0)
        curses.noecho()
        scr.addstr(1, 0, response)
        scr.addstr(max_y - 1, 1, "Press any key to quit")
        scr.getch()
        scr.nodelay(1)
        curses.noecho()

    def add_connection(scr, fullscreen=False):
        """
        Create a new sql connection and return it
        """
        (max_y, max_x) = scr.getmaxyx()
        if fullscreen:
             ques_pos = max_y - 1
        else:
             ques_pos = 3
        scr.nodelay(0)
        curses.echo()
        scr.move(ques_pos, 0)
        scr.clrtoeol()
        scr.addstr(ques_pos, 0, "backend : ")
        value = scr.getstr()
        if value != "":
            if value in sqltoplib.DISPONIBLE_BACKEND:
                backend = value
            else:
                scr.move(ques_pos, 0)
                scr.clrtoeol()
                scr.addstr(ques_pos, 0, 'Backend is not valid')
                scr.refresh()
                time.sleep(1)
                return None
        if backend == "mysql":
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "host [localhost] : ")
            value = scr.getstr()
            if value is "":
                host = "localhost"
            else:
                host = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "user [root] : ")
            value = scr.getstr()
            if value is "":
                user = "root"
            else:
                user = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "port [3306] : ")
            value = scr.getstr()
            if value is "":
                port  = 3306
            else:
                port = int(value)
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            curses.noecho()
            scr.addstr(ques_pos, 0, "password : ")
            value = scr.getstr()
            password = value
            new_pm = sqltoplib.create_connection(backend=backend, host=host, user=user, port=port, password=password)
        elif backend == "redisdb":
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "host [localhost] : ")
            value = scr.getstr()
            if value is "":
                host = "localhost"
            else:
                host = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "port [6379] : ")
            value = scr.getstr()
            if value is "":
                port  = 6379
            else:
                port = int(value)
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            curses.noecho()
            scr.addstr(ques_pos, 0, "password : ")
            value = scr.getstr()
            password = value
            new_pm = sqltoplib.create_connection(backend=backend, host=host, port=port, password=password)
        elif backend == "linux":
            new_pm = sqltoplib.create_connection(backend=backend)
        else:
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "host [localhost] : ")
            value = scr.getstr()
            if value is "":
                host = "localhost"
            else:
                host = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "user : ")
            value = scr.getstr()
            user = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "port : ")
            value = scr.getstr()
            port = int(value)
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            curses.noecho()
            scr.addstr(ques_pos, 0, "password : ")
            value = scr.getstr()
            password = value
            new_pm = sqltoplib.create_connection(backend=backend, host=host, user=user, port=port, password=password)
        try:
            new_pm.connect()
        except sqltoplib.processmanager.ProcessManagerError:
            pass
        scr.nodelay(1)
        curses.noecho()
        return new_pm

    def help(scr):
        """
        Display help
        """
        help_text = """
     Keyboard shortcut
     
     [a]dd          Add a new connection
     [c]onnect      Connect or disconnect
     [d]elay        Modify delay between refresh
     [e]dit         Edit current connection
     [E]xtension    Display extended functionality  
     [f]ilter       Filter process
     [F]ullscreen   Display in fullscreen mode
     [i]nfo         Get complete info on process
     [o]rder        Order process
     [p]aused       Pause
     [r]emove       Remove current connection
     [s]tats        Get complete stats about current connection
     [w]rite        Dump process to a csv file
     [h]elp         Display this help 
     [q]uit         Quit
     [:]            Interactive command
     
     Use up and down arrow to select process
     Use left and right arrow to navigate history
        """
        (max_y, max_x) = scr.getmaxyx()
        scr.erase()
        scr.nodelay(0)
        curses.noecho()
        scr.addstr(1, 0, help_text)
        scr.addstr(max_y - 1, 1, "Press any key to quit")
        scr.getch()
        scr.nodelay(1)
        curses.noecho()

    def edit_connection(scr, pm, fullscreen=False):
        """
        Edit a sql conection
        """
        reload_pm = False
        scr.nodelay(0)
        curses.echo()
        scr.move(3, 0)
        scr.clrtoeol()
        scr.addstr(3, 0, "host [ %s ] : " % (pm.host))
        value = scr.getstr()
        if value != "":
            pm.host = value
            reload_pm = True
        scr.move(3, 0)
        scr.clrtoeol()
        scr.addstr(3, 0, "user [ %s ] : " % (pm.user))
        value = scr.getstr()
        if value != "":
            pm.user = value
            reload_pm = True
        scr.move(3, 0)
        scr.clrtoeol()
        scr.addstr(3, 0, "port [ %s ] : " % (pm.port))
        value = scr.getstr()
        if value != "":
            pm.port = int(value)
            reload_pm = True
        scr.move(3, 0)
        scr.clrtoeol()
        curses.noecho()
        scr.addstr(3, 0, "password : ")
        value = scr.getstr()
        if value != "":
            pm.password = value
            reload_pm = True

        if reload_pm:
            pm.close()
            try:
                pm.connect()
            except:
                pass
        scr.nodelay(1)
    curses.noecho()

    def display_details(scr, process):
        """
        Display all info about a process
        """
        (max_y, max_x) = scr.getmaxyx()
        scr.erase()
        scr.nodelay(0)
        curses.curs_set(0)
        scr.addstr(0, 0, "Process infos")
        scr.addstr(2, 1, "Id", curses.A_BOLD)
        scr.addstr(3, 1, str(process.pid))
        scr.addstr(5, 1, "User", curses.A_BOLD)
        scr.addstr(6, 1, process.user)
        scr.addstr(8, 1, "Host", curses.A_BOLD)
        scr.addstr(9, 1, process.host)
        scr.addstr(11, 1, "Database", curses.A_BOLD)
        scr.addstr(12, 1, process.db)
        scr.addstr(14, 1, "State", curses.A_BOLD)
        scr.addstr(15, 1, process.state)
        scr.addstr(17, 1, "Time", curses.A_BOLD)
        scr.addstr(18, 1, str(datetime.timedelta(seconds=process.time)))
        scr.addstr(20, 1, "Info", curses.A_BOLD)
        try:
            info = sqlparse.format(process.info, reindent=True, keyword_case = "upper")
        except:
            info = process.info
        try:
            scr.addstr(22, 0, info)
        except _curses.error:
            scr.addstr(22, 0, "Sql request is too long to display")
        scr.addstr(max_y-1, 0, "Press any key to quit")
        scr.refresh()
        scr.getch()
        scr.nodelay(1)
        curses.curs_set(1)

    def add_filter(scr, pm, fullscreen=False):
        (max_y, max_x) = scr.getmaxyx()
        if fullscreen:
            ques_pos = max_y - 1
        else:
            ques_pos = 3
        key = ""
        scr.addstr(ques_pos, 0, '[p]id [u]ser [h]ost [d]atabase [s]tate [t]ime [i]nfo [r]eset : ')
        scr.nodelay(0)
        curses.echo()
        scr.refresh()
        key = scr.getch()
        if key == ord("p"):
            key = "pid"
        elif key == ord("u"):
            key = "user"
        elif key == ord("h"):
            key = "host"
        elif key == ord("d"):
            key = "db"
        elif key == ord("s"):
            key = "state"
        elif key == ord("t"):
            key = "time"
        elif key == ord("i"):
            key = "info"
        elif key == ord("r"):
            pm.del_all_filter()
            key = None
        else:
            key = None
        if key is not None:
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            txt_value = "Specify a value or regexp [ " + pm.get_filter(key) + " ] : "
            scr.addstr(ques_pos, 0, 'Specify a value or regexp [ %s ] : ' % (pm.get_filter(key)))
            #scr.move(3, len(txt_value))
            value = scr.getstr()
            if value == "":
                value = pm.get_filter(key)
            pm.add_filter(key, value)
            curses.noecho()
            scr.nodelay(1)
            scr.refresh()
        scr.nodelay(1)
        curses.noecho()

    def display_header(scr, pm, index, pms, fullscreen=False):
        """
        Display header info

        """
        (max_y, max_x) = scr.getmaxyx()
        if not fullscreen:
            total_task = 0
            filtered_task = 0
            if len(pm._filter) > 0:
                total_task = len(pm._process)
                filtered_task = len(pm.process)
            else:
                total_task = len(pm.process)
            if pm.is_online:
                status = "Online"
            else:
                status = "Offline"
            scr.addstr(0, 0, "Tasks : %s Total, %s filtered, Conn : %d / %d" % (str(total_task), str(filtered_task), index + 1, len(pms)))
            scr.addstr(1, 0, 'User : %s, Host : %s, Port : %s, Uptime : %s' % (pm.user[:10], pm.host[:15], pm.port, pm.uptime))
            scr.addstr(2, 0, 'backend : %s, Version : %s, Status : %s' % (pm.BACKEND, pm.version, status))
            if pm.BACKEND == "linux":
                scr.addstr(4, 0, '%-10s %-11s %-5s %-8s %-5s%s' % ("Pid", "User", "State", "Time", "Info", ' '*(max_x-39)), curses.A_BOLD|curses.A_REVERSE)
            elif pm.BACKEND == "Unknown":
                scr.addstr(4, 0, '%s' % (' '*(max_x)), curses.A_BOLD|curses.A_REVERSE)
            else:
                scr.addstr(4, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)
        else:
            if pm.BACKEND == "linux":
                scr.addstr(0, 0, '%-10s %-11s %-5s %-8s %-5s%s' % ("Pid", "User", "State", "Time", "Info", ' '*(max_x-39)), curses.A_BOLD|curses.A_REVERSE)
            elif pm.BACKEND == "Unknown":
                scr.addstr(0, 0, '%s' % (' '*(max_x)), curses.A_BOLD|curses.A_REVERSE)
            else:
                scr.addstr(0, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)
        if not pm.is_online and pm.error is not None:
            scr.addstr(3, 0, 'error : %s' % (pm.error))

    def display_footer(scr, text):
        """
        Display footer mainly for action choice from user
        """ 
        (max_y, max_x) = scr.getmaxyx()
        scr.addstr(max_y-1, 0, '%s' % (text), curses.A_BOLD | curses.A_REVERSE)
        scr.hline(max_y-1, len(text), " ", max_x, curses.A_BOLD | curses.A_REVERSE)

    def display_process(scr, pm=None, highlight=None, fullscreen=False):
        """
        Display process to screen
        """
        (max_y, max_x) = scr.getmaxyx()
        if fullscreen:
           cnt = 1
           max_process = max_y - 2
        else:
           cnt = 5
           max_process = max_y-6
        if highlight > len(pm.process):
            highlight = len(pm.process) - 1
        for process in pm.process[:(max_process)]:
            if highlight is not None:
                if highlight == (cnt - 5):
                    if pm.BACKEND == "linux":
                        scr.addstr(cnt, 0, '%-10s %-11s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.state, process.time, process.info[:44]), curses.A_REVERSE)
                    elif pm.BACKEND == "redisdb":
                        scr.addstr(cnt, 0, '%-11s %-5s %-8s %-5s' % (process.user, process.state, process.time, process.info[:44]), curses.A_REVERSE)
                    else:
                        scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]), curses.A_REVERSE)
                else:
                    if pm.BACKEND == "linux":
                        scr.addstr(cnt, 0, '%-10s %-11s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.state, process.time, process.info[:44]))
                    elif pm.BACKEND == "redisdb":
                        scr.addstr(cnt, 0, '%-11s %-5s %-8s %-5s' % (process.user, process.state, process.time, process.info[:44]))
                    else:
                        scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]))
            else:
                if pm.BACKEND == "linux":
                    scr.addstr(cnt, 0, '%-10s %-11s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.state, process.time, process.info[:44]))
                elif pm.BACKEND == "redisdb":
                    scr.addstr(cnt, 0, '%-11s %-5s %-8s %-5s' % (process.user, process.state, process.time, process.info[:44]))
                else:
                    scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]))
            cnt += 1



