package csu.wangke.keblog.controller;

import csu.wangke.keblog.service.PostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.IOException;

@Controller
@RequestMapping("/post")
public class PostController {
  @Autowired
  PostService postService = new PostService();

  @GetMapping("/child/{path}")
  public String getContent(@PathVariable String path) throws IOException {
    return postService.getPostContentByPath(path);
  }
}
