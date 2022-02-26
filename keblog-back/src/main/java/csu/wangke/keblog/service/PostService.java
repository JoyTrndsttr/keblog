package csu.wangke.keblog.service;

import csu.wangke.keblog.domain.PostFile;
import csu.wangke.keblog.utils.FileReadUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.Stack;

@Service
public class PostService {

  String PATH = "/Users/wangke/WebstormProjects/keblog/keblog-back/src/main/resources/static/posts";

  @Autowired
  FileReadUtil fileReadUtil = new FileReadUtil();

  public String getPostContentByPath(String path) throws IOException {

//    path = "/Users/wangke/WebstormProjects/keblog/keblog-back/src/main/resources/static/posts/八股/JS重新总结.md";
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

  public String getChartsContent() throws IOException {
    PostFile postFile = new PostFile(PATH);
    //用一个栈储存postFile用于递归
    Stack<PostFile> postStack = new Stack<>();
    //结果对象用result表示
    JSONObject result = new JSONObject();
    //用一个数组储存所有文件夹信息
    JSONArray array = new JSONArray();
    //单个文件夹信息
    JSONObject obj = new JSONObject();
    obj.put("name",postFile.name);
    obj.put("size",postFile.postList.size());
    postStack.push(postFile);
    while(!postStack.isEmpty()){
      postFile = postStack.pop();
      for (PostFile postFile1:postFile.postList){
        if(postFile1.status==0){
          //对于单个文件不与操作
        }
        else{
          //对于文件夹
          obj = new JSONObject();
          obj.put("name",postFile1.name);
          obj.put("size",postFile1.postList.size());
          array.add(obj);
          postStack.push(postFile1);
        }
      }
    }
    result.put("content",array);
    return result.toString();
  }
}
