import os, sys, argparse, asyncio

async def main():
	ArgsParser = argparse.ArgumentParser(description = 'Reads and writes data across network connections, using the TCP.')
	ArgsParser.add_argument('hostname', type = str, nargs = 1, help = 'remote hostname')
	ArgsParser.add_argument('port', type = int, nargs = 1, help = 'remote port number')
	ArgsParser.add_argument('-c', type = bool, nargs = '?', default = False, const = True, help = 'convert CRLF to LF')
	ArgsArgsParserResult = ArgsParser.parse_args()
	TCP_reader, TCP_writer = await asyncio.open_connection(host = ArgsArgsParserResult.hostname[0], port = ArgsArgsParserResult.port[0])
	if ArgsArgsParserResult.c:
		await asyncio.gather(handle_reader(TCP_reader), handle_writer(TCP_writer, Convert_CRLF_to_LF))
	else:
		await asyncio.gather(handle_reader(TCP_reader), handle_writer(TCP_writer))

async def handle_reader(reader):
	while True:
		data = await reader.readline()
		try:
			print(data.decode(), end='')
		except Exception as e:
			print(e)

async def handle_writer(writer, action = None):
	std_reader, _ = await open_stdio()
	while True:
		data = await std_reader.readline()
		if action:
			data = action(data)
		writer.write(data)
		await writer.drain()

def Convert_CRLF_to_LF(chunk):
	return chunk[:-2] + b'\n'

async def open_stdio(limit = asyncio.streams._DEFAULT_LIMIT, loop = None):
	if loop is None:
		loop = asyncio.get_event_loop()
	if sys.platform == 'win32':
		return _win32_stdio(loop)
	reader = asyncio.StreamReader(limit = limit, loop = loop)
	await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader, loop = loop), sys.stdin)
	writer_transport, writer_protocol = await loop.connect_write_pipe(lambda: asyncio.streams.FlowControlMixin(loop = loop), os.fdopen(sys.stdout.fileno(), 'wb'))
	writer = asyncio.streams.StreamWriter(writer_transport, writer_protocol, None, loop)
	return reader, writer

def _win32_stdio(loop):
	class Win32StdinReader:
		def __init__(self):
			self.stdin = sys.stdin.buffer 
		async def readline(self):
			return await loop.run_in_executor(None, self.stdin.readline)
	class Win32StdoutWriter:
		def __init__(self):
			self.buffer = []
			self.stdout = sys.stdout.buffer
		def write(self, data):
			self.buffer.append(data)
		async def drain(self):
			data, self.buffer = self.buffer, []
			return await loop.run_in_executor(None, sys.stdout.writelines, data)
	return Win32StdinReader(), Win32StdoutWriter()

asyncio.run(main())
