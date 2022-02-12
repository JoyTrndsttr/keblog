package csu.wangke.keblog;

import csu.wangke.keblog.domain.PostFile;
import csu.wangke.keblog.service.PostService;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

@SpringBootTest
class KeblogApplicationTests {

  @Test
  void contextLoads() {
  }

  @Test
  void testFiles() throws IOException {
    File file = new File("src/main/resources/static/posts/准备.md");

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
    System.out.println(postFile.content);
  }

  @Test
  void testRead() throws IOException{
    PostService postService = new PostService();
    System.out.println(postService.getPostContentByPath(""));;
  }

}
