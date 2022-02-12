package csu.wangke.keblog.utils;

import csu.wangke.keblog.domain.PostFile;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Service
public class FileReadUtil {

  public String readFile(String path) throws IOException {
    File file = new File(path);

//    FileInputStream fis = new FileInputStream(file);
//    byte[] buffer = new byte[10];
//    StringBuilder sb = new StringBuilder();
//    while (fis.read(buffer) != -1) {
//      sb.append(new String(buffer));
//      buffer = new byte[10];
//    }
//    fis.close();

    List<String> lines=new ArrayList<String>();
    BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(file),"UTF-8"));
    String line = null;
    while ((line = br.readLine()) != null) {
      lines.add(line);
    }
    br.close();
    String result=lines.get(0);
    for(int i=1;i<lines.size();i++) result=result + '\n'+lines.get(i);

    return result;
  }
}
