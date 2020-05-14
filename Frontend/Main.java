import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

// 1. 本程式必須與 TcpServer.java 程式搭配執行，先執行 TcpServer 再執行本程式。
// 2. 本程式必須有一個參數，指定伺服器的 IP。
// 用法範例： java TcpClient 127.0.0.1

public class Main {
    public static int port = 6666; // 設定傳送埠為 20。
    public static String address = "127.0.0.1";

    public static void main(String args[]) throws Exception {
        Socket client = new Socket(address, port);     // 根據 args[0] 的 TCP Socket.
        OutputStream out = client.getOutputStream();

        // send account package
        AccountPackage testAccount = new AccountPackage(258,200,20,5,16,"哈哈哈","是我啦",true);
        testAccount.setRequestAction(0);
        out.write(PackageHandler.accountPackageEncode(testAccount));
        //
        // send schedule package
//        SchedulePackage testSchedule = new SchedulePackage(5566, "對阿天氣真好", 30, 4, 21, 12, 248);
//        out.write(PackageHandler.schedulePackageEncode(testSchedule));
        //
        out.flush();
        InputStream in = client.getInputStream();      // 取得輸入訊息的串流
        BufferedReader s_in = new BufferedReader (new InputStreamReader(in, "UTF-8"));

        StringBuffer buf = new StringBuffer();        // 建立讀取字串。
        ByteBuffer b_buf = ByteBuffer.allocate(1024);
        try {
            while (true) {            // 不斷讀取。
                int x = in.read();    // 讀取一個 byte。(read 傳回 -1 代表串流結束)
                if (x==-1) break;    // x = -1 代表串流結束，讀取完畢，用 break 跳開。
                byte b = (byte) x;    // 將 x 轉為 byte，放入變數 b.
                b_buf.put(b);
                buf.append((char) b);// 假設傳送ASCII字元都是 ASCII。
            }
        } catch (Exception e) {
            in.close();                // 關閉輸入串流。
        }
        out.close();

        // deal with first 3 char
        byte[] resultArray = Arrays.copyOfRange(b_buf.array(), 3, b_buf.array().length);
        byte[] typeArray = Arrays.copyOfRange(b_buf.array(), 0, 3);
        String typeString = new String(typeArray, StandardCharsets.UTF_8);
//        System.out.println(typeString);
        if(typeString.equals("acc"))
        {
            AccountPackage rcvPkg = PackageHandler.accountPackageDecode(resultArray);
            System.out.println(rcvPkg.getMoney());
        }
        else if(typeString.equals("sch"))
        {
            SchedulePackage rcvPkg = PackageHandler.schedulePackageDecode(resultArray);
            System.out.println(rcvPkg.getTodo());
        }
        //


        System.out.println("message send.");                    // 印出接收到的訊息。
        client.close();                                // 關閉 TcpSocket.
    }
}