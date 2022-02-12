package csu.wangke.keblog.utils;

import csu.wangke.keblog.domain.PostFile;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

@Service
public class FileReadUtil {
  public String readFile(String path) throws IOException {
    File file = new File(path);

    FileInputStream fis = new FileInputStream(file);
    byte[] buffer = new byte[10];
    StringBuilder sb = new StringBuilder();
    while (fis.read(buffer) != -1) {
      sb.append(new String(buffer));
      buffer = new byte[10];
    }
    fis.close();
    PostFile postFile = new PostFile();
    postFile.content = sb.toString();
    return postFile.content;
  }
}
