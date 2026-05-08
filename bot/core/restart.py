import minescript as m
import bot.core.minescript_extra as m_extra
    
def restart(cmd:str="\\bot\\modes\\auto_miner") -> None:
    m.echo(f"{m_extra.txt_clr('y')}\nRestarting script...\n")
    m_extra.toggle_all(False)
    
    previews_jobs = m.job_info()
    new_job_id = None
    
    m_extra.eat_food()
    m.execute(cmd)
    
    for job in m.job_info():
        if job.job_id not in {p_job.job_id for p_job in previews_jobs}:
            new_job_id = job.job_id
            
    if (not new_job_id):
        m.echo(f"{m_extra.txt_clr('r')}Failed to start a new job")
        return
    
    for job in previews_jobs: 
        if (job.command == ["bot\\main"]) or (job.job_id == new_job_id):
            continue
        m.execute(f"\\killjob {job.job_id}")