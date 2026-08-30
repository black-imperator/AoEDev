// Standalone exercise of CvTaggedStream. No game, no DLL -- a mock stream over a byte
// vector is enough, and this is the one part of the save format that can be tested that
// way. Everything downstream trusts this encoding, so it is worth proving separately.
//
// build: clang++ -I"<src>" test_taggedstream.cpp "<src>/CvTaggedStream.cpp" -o t.exe

// FDataStreamBase.h names std::string in its signatures without including <string>;
// in the DLL build the umbrella header has already pulled it in.
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

#include "FDataStreamBase.h"
#include "CvTaggedStream.h"

static int g_iFailures = 0;

#define CHECK(cond, what) \
	do { \
		if (!(cond)) { \
			printf("  FAIL  %s\n", what); \
			g_iFailures++; \
		} \
	} while (0)

// Minimal FDataStreamBase over a growable buffer. Only the calls CvTaggedStream makes
// do anything; the rest exist because the interface is pure virtual.
class MemStream : public FDataStreamBase
{
public:
	MemStream() : m_iPos(0) {}

	std::vector<unsigned char> m_data;
	int m_iPos;

	void Rewind() { m_iPos = 0; }
	bool AtEnd() { return m_iPos >= (int)m_data.size(); }
	void FastFwd() { m_iPos = (int)m_data.size(); }
	unsigned int GetPosition() const { return (unsigned int)m_iPos; }
	void SetPosition(unsigned int p) { m_iPos = (int)p; }
	void Truncate() {}
	void Flush() {}
	unsigned int GetEOF() const { return (unsigned int)m_data.size(); }
	unsigned int GetSizeLeft() const { return (unsigned int)(m_data.size() - m_iPos); }
	void CopyToMem(void*) {}

	void put(const void* p, int n)
	{
		const unsigned char* s = (const unsigned char*)p;
		for (int i = 0; i < n; i++) m_data.push_back(s[i]);
	}
	void get(void* p, int n)
	{
		unsigned char* d = (unsigned char*)p;
		for (int i = 0; i < n; i++)
			d[i] = (m_iPos < (int)m_data.size()) ? m_data[m_iPos++] : 0;
	}

	unsigned int WriteString(const wchar*) { return 0; }
	unsigned int WriteString(const char*) { return 0; }
	unsigned int WriteString(const std::string&) { return 0; }
	unsigned int WriteString(const std::wstring&) { return 0; }
	unsigned int WriteString(int, std::string[]) { return 0; }
	unsigned int WriteString(int, std::wstring[]) { return 0; }
	unsigned int ReadString(char*) { return 0; }
	unsigned int ReadString(wchar*) { return 0; }
	unsigned int ReadString(std::string&) { return 0; }
	unsigned int ReadString(std::wstring&) { return 0; }
	unsigned int ReadString(int, std::string[]) { return 0; }
	unsigned int ReadString(int, std::wstring[]) { return 0; }
	char* ReadString() { return 0; }
	wchar* ReadWideString() { return 0; }

	void Read(char* v) { get(v, 1); }
	void Read(byte* v) { get(v, 1); }
	void Read(int n, char v[]) { get(v, n); }
	void Read(int n, byte v[]) { get(v, n); }
	void Read(bool* v) { get(v, sizeof(bool)); }
	void Read(int n, bool v[]) { get(v, n * sizeof(bool)); }
	void Read(short* v) { get(v, 2); }
	void Read(unsigned short* v) { get(v, 2); }
	void Read(int n, short v[]) { get(v, n * 2); }
	void Read(int n, unsigned short v[]) { get(v, n * 2); }
	void Read(int* v) { get(v, 4); }
	void Read(unsigned int* v) { get(v, 4); }
	void Read(int n, int v[]) { get(v, n * 4); }
	void Read(int n, unsigned int v[]) { get(v, n * 4); }
	void Read(long* v) { get(v, sizeof(long)); }
	void Read(unsigned long* v) { get(v, sizeof(long)); }
	void Read(int n, long v[]) { get(v, n * sizeof(long)); }
	void Read(int n, unsigned long v[]) { get(v, n * sizeof(long)); }
	void Read(float* v) { get(v, 4); }
	void Read(int n, float v[]) { get(v, n * 4); }
	void Read(double* v) { get(v, 8); }
	void Read(int n, double v[]) { get(v, n * 8); }

	void Write(char v) { put(&v, 1); }
	void Write(byte v) { put(&v, 1); }
	void Write(int n, const char v[]) { put(v, n); }
	void Write(int n, const byte v[]) { put(v, n); }
	void Write(bool v) { put(&v, sizeof(bool)); }
	void Write(int n, const bool v[]) { put(v, n * sizeof(bool)); }
	void Write(short v) { put(&v, 2); }
	void Write(unsigned short v) { put(&v, 2); }
	void Write(int n, const short v[]) { put(v, n * 2); }
	void Write(int n, const unsigned short v[]) { put(v, n * 2); }
	void Write(int v) { put(&v, 4); }
	void Write(unsigned int v) { put(&v, 4); }
	void Write(int n, const int v[]) { put(v, n * 4); }
	void Write(int n, const unsigned int v[]) { put(v, n * 4); }
	void Write(long v) { put(&v, sizeof(long)); }
	void Write(unsigned long v) { put(&v, sizeof(long)); }
	void Write(int n, const long v[]) { put(v, n * sizeof(long)); }
	void Write(int n, const unsigned long v[]) { put(v, n * sizeof(long)); }
	void Write(float v) { put(&v, 4); }
	void Write(int n, const float v[]) { put(v, n * 4); }
	void Write(double v) { put(&v, 8); }
	void Write(int n, const double v[]) { put(v, n * 8); }
};

enum { T_A = 1, T_B, T_C, T_D, T_E, T_F, T_UNKNOWN, T_BLOB };

static void testRoundTrip()
{
	printf("round trip of every scalar form\n");
	MemStream s;
	{
		CvTagWriter w(&s);
		w.write(T_A, (int)0);
		w.write(T_B, (int)-1);
		w.write(T_C, (int)2147483647);
		w.write(T_D, (int)(-2147483647 - 1));
		w.write(T_E, true);
		w.write(T_F, (short)-12345);
		w.writeBytes(T_BLOB, "hello", 5);
		w.end();
	}
	s.Rewind();

	CvTagReader r(&s);
	int a = 9, b = 9, c = 9, d = 9;
	bool e = false;
	int f = 9;
	char blob[8];
	memset(blob, 0, sizeof(blob));

	while (r.next())
	{
		switch (r.tag())
		{
		case T_A: a = r.asInt(); break;
		case T_B: b = r.asInt(); break;
		case T_C: c = r.asInt(); break;
		case T_D: d = r.asInt(); break;
		case T_E: e = r.asBool(); break;
		case T_F: f = r.asInt(); break;
		case T_BLOB: r.asBytes(blob, 5); break;
		default: r.skip(); break;
		}
	}

	CHECK(!r.bad(), "reader stayed healthy");
	CHECK(a == 0, "zero");
	CHECK(b == -1, "minus one");
	CHECK(c == 2147483647, "INT_MAX");
	CHECK(d == (-2147483647 - 1), "INT_MIN");
	CHECK(e == true, "bool");
	CHECK(f == -12345, "short");
	CHECK(memcmp(blob, "hello", 5) == 0, "byte block");
}

static void testUnknownTagIsSkipped()
{
	printf("a reader that does not know a tag keeps going\n");
	MemStream s;
	{
		CvTagWriter w(&s);
		w.write(T_A, 111);
		w.write(T_UNKNOWN, 999);          // future field
		w.writeBytes(T_BLOB, "xxxxxxxx", 8);
		w.write(T_B, 222);                 // must still arrive
		w.end();
	}
	s.Rewind();

	CvTagReader r(&s);
	int a = 0, b = 0, seen = 0;
	while (r.next())
	{
		seen++;
		switch (r.tag())
		{
		case T_A: a = r.asInt(); break;
		case T_B: b = r.asInt(); break;
		default: r.skip(); break;      // pretends not to know T_UNKNOWN / T_BLOB
		}
	}

	CHECK(!r.bad(), "reader stayed healthy across unknown fields");
	CHECK(seen == 4, "saw every field");
	CHECK(a == 111, "field before the unknown one");
	CHECK(b == 222, "field AFTER the unknown one still decoded");
}

static void testMissingFieldKeepsDefault()
{
	printf("a field the writer omitted keeps its default\n");
	MemStream s;
	{
		CvTagWriter w(&s);
		w.write(T_A, 5);
		w.end();
	}
	s.Rewind();

	int a = 0, b = 4242;      // b stands in for a reset() default
	CvTagReader r(&s);
	while (r.next())
	{
		switch (r.tag())
		{
		case T_A: a = r.asInt(); break;
		case T_B: b = r.asInt(); break;
		default: r.skip(); break;
		}
	}
	CHECK(a == 5, "present field read");
	CHECK(b == 4242, "absent field untouched");
}

static void testRecordIsSelfContained()
{
	printf("a record does not run into the next one\n");
	MemStream s;
	{
		CvTagWriter w(&s);
		w.write(T_A, 1);
		w.write(T_B, 2);
		w.end();
	}
	s.Write((int)0x5EA15EA1);   // sentinel written straight after the record
	s.Rewind();

	{
		CvTagReader r(&s);
		while (r.next()) r.skip();
		CHECK(!r.bad(), "record parsed");
	}
	int iSentinel = 0;
	s.Read(&iSentinel);
	CHECK(iSentinel == 0x5EA15EA1, "stream positioned exactly after the record");
}

static void testSizeAgainstPositional()
{
	printf("size against the positional format\n");
	MemStream s;
	{
		CvTagWriter w(&s);
		// A unit-ish object: mostly small or zero, which is the real distribution.
		for (int i = 1; i <= 200; i++)
		{
			w.write(i, (i % 17 == 0) ? i * 3 : 0);
		}
		w.end();
	}
	const int iTagged = (int)s.m_data.size();
	const int iPositional = 200 * 4;
	printf("    tagged %d bytes, positional %d bytes (%+d%%)\n",
		iTagged, iPositional, (iTagged - iPositional) * 100 / iPositional);
	CHECK(iTagged < iPositional, "tagged is smaller than positional for typical data");
}

int main()
{
	testRoundTrip();
	testUnknownTagIsSkipped();
	testMissingFieldKeepsDefault();
	testRecordIsSelfContained();
	testSizeAgainstPositional();

	printf("\n%s\n", g_iFailures == 0 ? "all checks passed" : "FAILURES ABOVE");
	return g_iFailures == 0 ? 0 : 1;
}
