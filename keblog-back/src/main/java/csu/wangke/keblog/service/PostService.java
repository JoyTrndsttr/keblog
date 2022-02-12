package csu.wangke.keblog.service;

import csu.wangke.keblog.utils.FileReadUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class PostService {

  @Autowired
  FileReadUtil fileReadUtil = new FileReadUtil();

  public String getPostContentByPath(String path) throws IOException {
    path = "/Users/wangke/WebstormProjects/keblog/keblog-back/src/main/resources/static/posts/准备.md";
    String result = fileReadUtil.readFile(path);
    return result;
  }
}
