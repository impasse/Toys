using System;
using System.IO;
using System.Threading;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Register
{
    public partial class Register : Form
    {
        public Register()
        {
            InitializeComponent();
            comboBox1.SelectedIndex = 0;
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void radioButton3_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private bool checkNotEmpty()
        {
            if (server.Text.Length == 0 || name.Text.Length == 0 || idnum.Text.Length==0)
            {
                return true;
            }else
            {
                return false;
            }
        }

        private String sendToServer(String serverHost,byte[] data)
        {
            try
            {
                IPEndPoint addr = new IPEndPoint(IPAddress.Parse(serverHost), 20009);
                Socket socket = new Socket(SocketType.Dgram, ProtocolType.Udp);
                //socket.SetSocketOption(SocketOptionLevel.Udp, SocketOptionName.ReceiveTimeout, true);
                socket.ReceiveTimeout = 1000;
                socket.SendTimeout = 1000;
                socket.SendTo(data, addr);
                byte[] bytes = new byte[1024];
                EndPoint serveraddr = addr;
                socket.ReceiveFrom(bytes, ref serveraddr);
                return Encoding.UTF8.GetString(bytes);
            }catch(Exception e)
            {
                return e.Message;
            }
        }

        public byte[] buildPacket()
        {
            using (StringWriter sw = new StringWriter())
            {
                sw.Write(name.Text + ",");
                sw.Write(comboBox1.SelectedIndex);
                if (radioButton1.Checked)
                {
                    sw.Write(",1班,");
                }else if (radioButton2.Checked)
                {
                    sw.Write(",2班,");
                }else if (radioButton3.Checked)
                {

                    sw.Write(",3班,");
                }
                else
                {
                    sw.Write(",4班,");
                }
                sw.Write(idnum.Text);
                return Encoding.UTF8.GetBytes(sw.ToString());
            }
        }

        void thread_call(object obj)
        {
            MessageBox.Show(sendToServer(server.Text, (byte[])obj));
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (checkNotEmpty())
            {
                MessageBox.Show("输入不能为空");
            }else{
                new Thread(thread_call).Start(buildPacket());
            }
        }
    }
}
