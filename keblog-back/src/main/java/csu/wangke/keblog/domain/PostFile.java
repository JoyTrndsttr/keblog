package csu.wangke.keblog.domain;

import java.util.ArrayList;

public class PostFile{
  //status=0代表文章，status=1代表文件夹
  public int status=0;
  public String name;
  public String url;
  public String content;
  public ArrayList<PostFile> postList = new ArrayList<>();

  public void add(PostFile postFile){
    postList.add(postFile);
  }

  public void delete(int index){

  }

  public PostFile getChild(int index){
    return postList.get(index);
  }

  public ArrayList<PostFile> getAllChild(){
    return postList;
  }

}
