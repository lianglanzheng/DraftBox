namespace RecycleDesktopLib
{
    public class FileDelete
    {
        private const int FO_DELETE = 0x3;
        private const ushort FOF_NOCONFIRMATION = 0x10;
        private const ushort FOF_ALLOWUNDO = 0x40;

        [System.Runtime.InteropServices.DllImport("shell32.dll", SetLastError = true, CharSet = System.Runtime.InteropServices.CharSet.Unicode)]
        private static extern int SHFileOperation([System.Runtime.InteropServices.In, System.Runtime.InteropServices.Out] _SHFILEOPSTRUCT str);
        [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential, CharSet = System.Runtime.InteropServices.CharSet.Unicode)]

        public class _SHFILEOPSTRUCT
        {
            public System.IntPtr hwnd;
            public System.UInt32 wFunc;
            public string pFrom;
            public string pTo;
            public System.UInt16 fFlags;
            public System.Int32 fAnyOperationsAborted;
            public System.IntPtr hNameMappings;
            public string lpszProgressTitle;
        }

        public static int MovetoRecycleBin(string path)
        {
            _SHFILEOPSTRUCT pm = new _SHFILEOPSTRUCT();
            pm.wFunc = FO_DELETE;
            pm.pFrom = path + '\0';
            pm.pTo = null;
            pm.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION;
            return SHFileOperation(pm);
        }
    }

    public class TargetSelect
    {
        public static string GetDesktopPath()
        {
            return System.Environment.GetFolderPath(System.Environment.SpecialFolder.Desktop);
        }
        
        public static string[] GetFilesList(string path)
        {
            return MergerArray(System.IO.Directory.GetDirectories(path), System.IO.Directory.GetFiles(path));
        }

        public static string[] MergerArray(string[] First, string[] Second)
        {
            string[] result = new string[First.Length + Second.Length];
            First.CopyTo(result, 0);
            Second.CopyTo(result, First.Length);
            return result;
        }
        public static bool IsFileVisible(string path)
        {
            return (new System.IO.FileInfo(path).Attributes & System.IO.FileAttributes.Hidden) != System.IO.FileAttributes.Hidden;
        }
    }
}

namespace RecycleDesktop
{
    class Program
    {
        static void Main(string[] args)
        {
            string DesktopPath = RecycleDesktopLib.TargetSelect.GetDesktopPath();
            string[] FilesList = RecycleDesktopLib.TargetSelect.GetFilesList(DesktopPath);
            foreach (string i in FilesList)
            {
                if (RecycleDesktopLib.TargetSelect.IsFileVisible(i))
                {
                    System.Console.Write(i + "\t");
                    System.Console.WriteLine(RecycleDesktopLib.FileDelete.MovetoRecycleBin(i));
                }
            }
        }
    }
}
