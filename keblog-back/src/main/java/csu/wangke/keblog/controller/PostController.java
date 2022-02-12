package csu.wangke.keblog.controller;

import csu.wangke.keblog.service.PostService;
import csu.wangke.keblog.utils.FileReadUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
@RequestMapping("/api/post")
public class PostController {
//  @Autowired
//  PostService postService = new PostService();

  @GetMapping("/child")
  public String getContent(String path) throws IOException {
    PostService postService = new PostService();
    String result = postService.getPostContentByPath("");
    return result;
  }
}
