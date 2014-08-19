def date_from_webkit(webkit_timestamp):
    """Convert date from webkit to normal date."""
    time = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=int(webkit_timestamp))
    if time.year < 1900:
        return "-"*10
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")

def zipdir(path, zip):
    """Very simple folder zip function."""
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))
