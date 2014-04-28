import datetime, re
import util


def max(db, r):
  pass
def record(db, r):
  path = r.path.split("/")
  key = path[3]
  func = path[4].upper()
  where = getRange(r.args["start"])

  if key == "dayrain" and func == "MAX":
    sql = """
      SELECT
        sum(rain) AS dayrain, 
        concat(substring(from_unixtime(datetime), 1,11),'00:00:00') AS datetime
      FROM
        archive
      {0}
    """.format(where)
  elif func == "SUM":
    sql = """
      SELECT
        sum({0}) AS {0}
      FROM
        archive
      {1}
    """.format(key, where)
  else:
    sql = ""

  result = db.select(sql)[0]

  return [unitConv(result)]

def now(db, r):
  result = {}
  d = datetime.datetime.today()
  today = util.getDate2UT(d.strftime("%Y-%m-%d"))
  sql = "SELECT * FROM archive WHERE datetime >= {0} ORDER BY datetime DESC LIMIT 1".format(today)
  result = db.select(sql)[0]
  sql = "SELECT SUM(rain) FROM archive WHERE datetime >= {0}".format(today)
  result.update({"dayrain": db.select(sql)[0].values()[0]})
  return [unitConv(result)]

def day(db, r):
  pass
def recent(db, r):
  sql = "SELECT * FROM archive ORDER BY datetime DESC LIMIT 60"
  result1 = db.select(sql)
  sql = "SELECT sum(rain) as dayrain FROM archive ORDER BY datetime DESC LIMIT 60"
  result2 = db.select(sql)[0]
  result = []
  for i in result1:
    i['dayrain'] = result2['dayrain']
    i['datetime'] = util.getDate(i['datetime'])
    result.append(unitConv(i))
    
  return result

def station(db, r):
  pass
def windhist(db, r):
  pass
def hour(db, r):
  where = getRange(r.args["start"])
  sql = """SELECT
    concat(substring(from_unixtime(datetime), 1,14),'00:00') AS datetime,
    AVG(outtemp) AS outtemp,
    MIN(outtemp) AS tempmin,
    MAX(outtemp) AS tempmax,
    AVG(dewpoint) AS dewpoint,
    AVG(rain) AS rain,
    AVG(windspeed) AS windspeed,
    MAX(windgust) AS windgust,
    AVG(winddir) AS winddir,
    AVG(barometer) AS barometer,
    AVG(outhumidity) AS outhumidity,
    AVG(intemp) AS intemp,
    AVG(inhumidity) AS inhumidity,
    AVG(heatindex) AS heatindex,
    AVG(windchill) AS windchill,
    AVG(UV) AS UV
    FROM archive
    {0}
    GROUP BY 1
    ORDER BY datetime 
  """.format(where)

  sql_result1 = db.select(sql)
  
  sql = """
    SELECT
      sum(rain) AS dayrain,
      concat(substring(from_unixtime(datetime), 1,14),'00:00') AS unit
    FROM
      archive
    {0}
    group by unit
  """.format(where)

  sql_old = """
    SELECT DISTINCT
      CONCAT(SUBSTRING(from_unixtime(datetime), 1,14),'00:00') AS unit,
      (SELECT
         sum(rain)
       FROM
         archive
       WHERE
         concat(substring(from_unixtime(datetime), 1,14),'00:00') = unit)
       AS dayrain
     FROM
       archive
     {0}
     ORDER BY 1
  """.format(where)
  sql_result2 = db.select(sql)

  result = []
  for r2 in sql_result2:
    for r in sql_result1:
      if r2["unit"] == r["datetime"]:
        r.update({"dayrain":r2["dayrain"]})
        result.append(unitConv(r))
  return result
    
def month(db, r):
  pass

def unitConv(data):
  new_data = {}
  p = re.compile('.*Temp[1-9]$')
  for k, v in data.items():
    if v == None:
      new_data.update({k:"null"})
    elif k in ["tempmin","outtemp", "tempmax", "intemp", "outTemp", "inTemp", "windchill", "dewpoint", "heatindex"]:
      new_data.update({k:f2c(v)})
    elif p.match(k) != None:
      new_data.update({k:f2c(v)})
    elif k in []:
      new_data.update({k:feet2mater(v)})
    elif k in ["pressure", "barometer", "altimeter"]:
      new_data.update({k:inhg2hpa(v)})
    elif k in ["rain","dayrain"]:
      new_data.update({k:inch2mm(v)})
    elif k in ["dateTime"]:
      new_data.update({k:util.getDate(v)})
    elif k in ["windSpeed"]:
      new_data.update({k:mph2mps(v)})
    elif k in ["UV", "inhumidity", "outhumidity", "windgust", "windspeed", "winddir"]:
        new_data.update({k:round(float(v),1)})
    else:
        new_data.update({k:v})

  return new_data

def getRange(start):
  if start.upper() == "3DAY":
    between_from = "unix_timestamp(now() - INTERVAL 3 DAY)"
    between_to = "unix_timestamp(now())"
  elif start.lower() == "yesterday":
    between_from = "unix_timestamp(now() - INTERVAL 1 DAY)"
    between_to = "unix_timestamp(now())"
  elif start.upper() == "WEEK":
    between_from = "unix_timestamp(now() - INTERVAL 1 WEEK)"
    between_to = "unix_timestamp(now())"
  elif start.upper() == "MONTH":
    between_from = "unix_timestamp(now() - INTERVAL 1 MONTH)"
    between_to = "unix_timestamp(now())"
  elif start.upper() == "YEAR":
    between_from = "unix_timestamp(now() - INTERVAL 1 YEAR)"
    between_to = "unix_timestamp(now())"

  if start.upper() == "TODAY":
    between_from = "unix_timestamp(CONCAT(SUBSTRING(now(), 1,11),'00:00:00'))"
    between_to = "unix_timestamp(now())"

  where = "WHERE datetime BETWEEN {0} AND {1}".format(between_from, between_to)
  return where

def f2c(v):
  return round((float(v)-32)*5/9, 1)

def feet2mater(v):
  return round(float(v)*0.3048, 1)

def inhg2hpa(v):
  return int(float(v)/0.0295)

def inch2mm(v):
  return int(float(v)*25.4)

def mph2mps(v):
  return round(float(v)*0.44704, 1)

