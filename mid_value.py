
def moving_average(timeseries[int], k: int):
    result = []
    current_sum = sum(timeseries[0:k])
    result.append(current_sum / k)
    for i in range(0, len(timeseries) - k):
        current_sum -= timeseries[i]
        current_sum += timeseries[i + k]
        current_avg = current_sum / k
        result.append(current_avg)
    return result         

if __name__ == '__main__':
    n = int(input())
    q = list(map(int, input().split()))
    k = list(input())
    
    result = moving_average(timeseries: List[int], k: int)
    print(' '.join(map(str, result)))
