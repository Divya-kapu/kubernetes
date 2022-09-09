#---tested for this url http://127.0.0.1:5000/a?vf=300&vi=5 , http://127.0.0.1:5000/a/metrics ----#
from urllib.parse import urlparse
from flask import Response, Flask, request
import prometheus_client
from prometheus_client import  Counter, Histogram  # other metrics are Summary, Gauge
import time
import json

app = Flask(__name__)

_INF = float("inf")
graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.',
                        buckets=(1, 2, 5, 6, 10, _INF))

def a_data_fetch_func(query_value_split1, sum,res_dct,path):
  for i in range(0, len(query_value_split1), 2):
    res_dct[i] = {query_value_split1[i]: query_value_split1[i + 1]}
    if int(query_value_split1[i + 1]) > int(sum):
      sum = int(query_value_split1[i + 1]) // sum
    else:
      sum = sum // int(query_value_split1[i + 1])

  sum1 = {path: sum}
  json_object = json.dumps(sum1, indent=4)
  return json_object

def a_func(url):
  result = urlparse(url)
  path = result.path
  res_dct = {}
  a_sum = 1
  query_value = result.query
  # query_value = f'"{result.query}"'
  query_value_list = query_value.replace("&", " ")
  query_value_list2 = query_value_list.replace("=", " ")
  query_value_split1 = query_value_list2.split(" ")
  if result.path == '/a':
    result1 = a_data_fetch_func(query_value_split1, a_sum,res_dct,path)
    return result1

@app.route("/a")
def main():
  start = time.time()
  graphs['c'].inc()
  time.sleep(0.600)
  end = time.time()
  graphs['h'].observe(end - start)
  url = request.url
  url_response = a_func(url)
  return url_response #

@app.route("/metrics")
def requests_count():
  res = []
  for k, v in graphs.items():
    res.append(prometheus_client.generate_latest(v))
  return Response(res, mimetype="text/plain")

