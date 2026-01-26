import time
import threading

import minescript as m
import bot.core.minescript_extra as m_extra

from bot.core.restart import restart

MODES = { # TODO: CHANGE COMPLETELY
    "descend": (m.execute, "\\bot\\modes\\test"),
    "auto": (m.execute, "\\bot\\modes\\auto_miner"),
    "scan": (m.execute, "\\bot\\modes\\scan_only"),
    "stop": (m_extra.kill_jobs, None),
    "stop all": (m_extra.kill_jobs, True),
    "restart": (restart, None),
    "help": (m_extra._help, None),
}

stop_flag = False


def commands(msg:str):
    if (not msg.startswith(".bot")):
        return
    
    msg = msg.replace(".", " ").replace("_", " ").split()
    
    if len(msg) > 3:
        m.echo(f"{m_extra.txt_clr('y')}Get help typing: .bot help")
        return
    
    cmd = msg[1].lower()
    
    if cmd in MODES:
        m.echo(f"Running mode: {m_extra.txt_clr('p')}{cmd}")
        try:
            executor, cmd = MODES[cmd]
            executor(cmd) if cmd else executor()
        except BaseException as e:
            m.echo(f"Error: {e}")
            executor, cmd = MODES["stop main"]
            executor(cmd)
            
            
    else: 
        m.echo(f"Unrecognizable mode: {cmd}")
        m.echo(f"{m_extra.txt_clr('y')}Get help typing: .bot help")


def main():
    global stop_flag
    m.echo(f"{m_extra.txt_clr('g')}Bot ACTIVATED\nUse: '.bot <mode>'")
    
    with m.EventQueue() as events:
        events.register_outgoing_chat_interceptor(prefix=".bot")
        m.echo(f"{m_extra.txt_clr('g')}Type '.bot stop' to STOP the program")
    
        while (not stop_flag):
            event = events.get()
            
            if event.type == m.EventType.OUTGOING_CHAT_INTERCEPT:
                message = event.message.strip()
                
                if ".bot stop all" == message.lower():
                    m.echo(f"{m_extra.txt_clr('g')}STOPPING SCRIPT...")
                    stop_flag = True

                threading.Thread(target=commands,
                                 args=(message,),
                                 daemon=True).start()
            
        time.sleep(0.1)
        

if __name__ == "__main__":
    main()