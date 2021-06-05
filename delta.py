def calculateDelta(bestLapDataDict : dict, currentLapData : tuple) -> float:
    currentLapDistance, currentLapTime = currentLapData

    absDiffFunction = lambda value : abs(value - currentLapDistance)
    closestDistance = min(bestLapDataDict.keys(), key=absDiffFunction)

    return currentLapTime - bestLapDataDict[closestDistance]