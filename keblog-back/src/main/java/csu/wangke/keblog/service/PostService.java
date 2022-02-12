package csu.wangke.keblog.service;

import csu.wangke.keblog.domain.PostFile;
import csu.wangke.keblog.utils.FileReadUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class PostService {

  @Autowired
  FileReadUtil fileReadUtil = new FileReadUtil();

  public String getPostContentByPath(String path) throws IOException {

    path = "/Users/wangke/WebstormProjects/keblog/keblog-back/src/main/resources/static/posts/准备.md";
    //首先判断Post为单个文章还是文件夹
    System.out.println(path);
    PostFile postFile = new PostFile(path);
    JSONObject result;
    if(postFile.status==0){
      //对文章直接获取内容
      result = new JSONObject();
      result.put("status",0);
      result.put("content",postFile.content);
    }
    else{
      //对文件夹获取其中的每个文件（文件名与地址）
      result = new JSONObject();
      result.put("status",1);
      JSONArray files = new JSONArray();
      for(int i=0;i<postFile.postList.size();i++){
        JSONObject file = new JSONObject();
        file.put("name", postFile.postList.get(i).name);
        file.put("path", postFile.postList.get(i).path);
        files.add(file);
      }
      result.put("content",files);
    }
    System.out.println(result);
    return result.toString();
  }
}
