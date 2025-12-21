import minescript, math
from bot.core.player import player

def priorityGroup(clusters, ore = 'diamond'):
    if len(clusters) == 1: 
        minescript.echo(f'Going to group of {ore}s at {clusters[0]['center']} (closest)')
        return clusters[0]
    close_to_player = 5
    
    for cluster in clusters:
        x, y, z = cluster['center']
        dist = math.sqrt((player.x - x)**2 + (player.y - y)**2 + (player.z - z)**2)
        cluster['distance'] = dist
    
    clusters_close = [cluster for cluster in clusters if cluster['distance'] <= close_to_player]
    
    if clusters_close: #Mine closer clusters first
        if len(clusters_close) == 1: return clusters_close[0]
        best_cluster, best_score = clusters_close[0], float('inf')
        
        for cluster in clusters_close:
            score = (1.5 * cluster['distance']) - (cluster['size'] * 2)
            
            if score <= best_score:
                best_score = score
                best_cluster = cluster
        
        minescript.echo(f'Going to group of {ore}s at {best_cluster['center']} (closest)')
        return best_cluster
    
    #No diamonds close to the player, try to find the largest with with travel less distance
    best_cluster = min(clusters, key=lambda cluster: (-(cluster['size']), cluster['distance']))
    minescript.echo(f'Going to group of {ore}s at {best_cluster['center']} (largest and closest)')
    return best_cluster