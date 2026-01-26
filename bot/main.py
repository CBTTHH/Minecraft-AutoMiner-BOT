import time
import threading

import minescript as m
import bot.core.minescript_extra as m_extra

from bot.core.restart import restart

MODES = { 
    "descend": (m.execute, "\\bot\\modes\\descend"),
    "auto": (m.execute, "\\bot\\modes\\auto_miner"),
    "scan": (m.execute, "\\bot\\modes\\scan_only"),
    "stop": (m_extra.kill_jobs, None),
    "stop all": (m_extra.kill_jobs, True),
    "restart": (restart, None),
    "help": (m_extra._help, None),
}


def main_running() -> bool:
    running_jobs = m.job_info()
    n_running_jobs = len(running_jobs) - 1
    
    if (not n_running_jobs):
        return False
    
    for job in running_jobs:
        if (job.command == ["bot\\main"]):
            m.echo(f"{m_extra.txt_clr('y')}\nMain script is already running\n")
            return True
    return False


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
            executor, cmd = MODES["stop all"]
            executor(cmd) if cmd else executor()
            
            
    else: 
        m.echo(f"Unrecognizable mode: {cmd}")
        m.echo(f"{m_extra.txt_clr('y')}Get help typing: .bot help")


def main():
    stop_flag = False
    
    m.echo(f"{m_extra.txt_clr('g')}Bot ACTIVATED\nUse: '.bot <mode>'")
    
    with m.EventQueue() as events:
        events.register_outgoing_chat_interceptor(prefix=".bot")
        m.echo(f"{m_extra.txt_clr('g')}Type '.bot stop' to STOP the program")
    
        while (not stop_flag):
            event = events.get()
            
            if event.type == m.EventType.OUTGOING_CHAT_INTERCEPT:
                message = event.message.strip().lower()
                
                if ".bot stop all" == message:
                    m.echo(f"{m_extra.txt_clr('g')}STOPPING SCRIPT...")
                    stop_flag = True

                threading.Thread(target=commands,
                                 args=(message,),
                                 daemon=True).start()
            
        time.sleep(0.1)
        

if __name__ == "__main__":
    running = main_running()
    if (not running):
        main()