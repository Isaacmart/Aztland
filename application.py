from io import StringIO
import os


def application(environ, start_response):
    headers = []
    headers.append(('Content-Type', 'text/plain'))
    write = start_response('200 OK', headers)

    input = environ['wsgi.input']
    output = StringIO()


    print("PID: %s" % os.getpid(), file=output)
    print("UID: %s" % os.getuid(), file=output)
    print("GID; %s" % os.getgid(), file=output)
    print(file=output)
    #print >> output, "PID: %s" % os.getpid()
    #print >> output, "UID: %s" % os.getuid()
    #print >> output, "GID: %s" % os.getgid()
    #print >> output

    keys = environ.keys()
    #keys.sort()
    for key in keys:
        print('%s: %s' % (key, repr(environ[key])), file=output)
        #print >> output, '%s: %s' % (key, repr(environ[key]))
    print(file=output)    
    #print >> output

    output.write(input.read(int(environ.get('CONTENT_LENGTH', '0'))))

    return [output.getvalue()]



