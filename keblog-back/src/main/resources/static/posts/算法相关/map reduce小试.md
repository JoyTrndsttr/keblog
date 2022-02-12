#### [生成平衡数组的方案数](https://leetcode-cn.com/problems/ways-to-make-a-fair-array/)

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
var waysToMakeFair = function(nums) {
    var result = 0
    //先把每个点后面的奇数index和与偶数index和存到数组里
    var m = []
    m.push([nums[0],0])//m先存到该元素奇数和偶数的和
    for(let i=1;i<nums.length;i++){
        if(i%2===0) m.push([m[i-1][0]+nums[i],m[i-1][1]])
        else if(i%2===1) m.push([m[i-1][0],m[i-1][1]+nums[i]])
    }
    var odd = nums.reduce((a,b,index)=>index%2===0?a+=b:a,0)//所有奇数和
    var even = nums.reduce((a,b,index)=>index%2===1?a+b:a,0)//所有偶数和
    //m[index-1] 为到该元素位置，前面的奇数和偶数和
    //n[i]为到该元素位置，后面的奇数和偶数和
    n = m.map(value => [odd-value[0],even-value[1]])
    //删除一个点
    nums.map((value,index)=>{
        var oddSum,evenSum;
        if(index===0){
            oddSum  = n[index][1]
            evenSum = n[index][0]
        }
        else{
            oddSum  = m[index-1][0] + n[index][1]
            evenSum = m[index-1][1] + n[index][0]
        }
        if(oddSum===evenSum) result++
    })
    return result
};
```