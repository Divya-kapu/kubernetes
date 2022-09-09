#-----test case url  curl http://127.0.0.1:5000/dv?vf=200&vi=5 , http://127.0.0.1:5000/dv/metrics ---#

from flask import Response, Flask, request
import json
from urllib.parse import urlparse
import prometheus_client
from prometheus_client import  Counter, Histogram  # other metrics are Summary, Gauge
import time

app = Flask(__name__)

_INF = float("inf")
graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.',
                        buckets=(1, 2, 5, 6, 10, _INF))

def dv_data_fetch_func(query_value_split1,sum,res_dct,path):
  print('dv_funcsum' , sum)
  for i in range(0, len(query_value_split1), 2):
    res_dct[i] = {query_value_split1[i]: query_value_split1[i + 1]}
    if (query_value_split1[i] != 't'):
      if (int(query_value_split1[i + 1]) > int(sum)) :
        sum = abs(sum - int(query_value_split1[i + 1]))
      else:
        sum = sum - int(query_value_split1[i + 1])
  sum1 = {path: sum}
  json_object = json.dumps(sum1, indent=4)
  return json_object

# @app.route('/')
# def hello():
#     return request.url
def dv_call_func(url):
  result = urlparse(url)
  path = result.path
  res_dct = {}
  dv_sum = 0
  query_value = result.query
  # query_value = f'"{result.query}"'
  query_value_list = query_value.replace("&", " ")
  query_value_list2 = query_value_list.replace("=", " ")
  query_value_split1 = query_value_list2.split(" ")
  if result.path == '/dv':
    result1 = dv_data_fetch_func(query_value_split1, dv_sum,res_dct,path)
    return result1

@app.route("/dv")
def main():
  start = time.time()
  graphs['c'].inc()
  time.sleep(0.600)
  end = time.time()
  graphs['h'].observe(end - start)
  url = request.url
  url_response = dv_call_func(url)
  return url_response  #

@app.route("/metrics")
def requests_count():
  res = []
  for k, v in graphs.items():
    res.append(prometheus_client.generate_latest(v))
  return Response(res, mimetype="text/plain")
