fields @timestamp, @message, @logStream

| filter @message like /(?i)(ERROR|Exception| 5\d{2} )/
| stats count(*) as errorCount by bin(5m) as timeWindow

| sort timeWindow desc
| limit 20
