#include<iostream>
#include<vector>

using namespace std;
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int len_nums = sizeof(nums);
        for(int i=0; i<len_nums; i++)
        {
            for(int j=i; j<len_nums; j++)
            {
                int sums = nums[i]+nums[j];
                if(sums == target)
                {
                    cout<<"数组的坐标为：["<< i<<","<< j<<"]"<<endl;
                }
//                else{
//                    cout<<"episod书虫"<<endl;
//                }
            }

        }
    }
};

int main()
{
//    vector<int> ilist {1,2,3.0,4,5,6,7};
    int arr[]= {2, 7, 11, 15};
    vector<int> nums(arr,arr+4);
    int target = 9;
    Solution calc;
    vector<int> nums_array = calc.twoSum(nums, target);
//    for(int i=0; i<nums_array.size(); i++)
//    {
//        cout<<nums_array[i]<<endl;
//    }
    return 0;
}
