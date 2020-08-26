pragma solidity ^0.5.9;
pragma experimental ABIEncoderV2;
// this is a skeleton file for the channel contract. Feel free to change as you wish. 
contract Validator{
    
    function is_valid_question(bytes32[] calldata lquestion) pure external returns(bool){
        bytes32[] memory question = lquestion;
        return question.length == 3 && question[0] != 0;
    }
    
    function is_answer_correct(bytes32[] calldata lquestion, bytes32[] calldata lanswer) pure external returns(bool){
        bytes32[] memory question = lquestion;
        bytes32[] memory answer = lanswer;
        require(answer.length == 2, "Answer length should be 2.");
        int a = bytes32_to_uint(question[0]); //8
        int b = bytes32_to_uint(question[1]); //77
        int c = bytes32_to_uint(question[2]); //87
        int d = bytes32_to_uint(answer[0]); //5
        int e = bytes32_to_uint(answer[1]); //4
        
        int e_abs = e;
        if(e < 0) {
            e_abs = -e;
        }
        int e_red = e;
        int mult = 1000000;
        while(e_red / 10 > 1 && mult > 1) {
            e_red = e_red / 10;
            mult = mult / 10;
        }
        int zero = (a * d + (b - c) * e) * mult;
        int zero2 = (- a * d + (b - c) * e) * mult;
        bool is_correct = (zero < e_abs && zero > -e_abs) || (zero2 < e_abs && zero2 > -e_abs);
        int[] memory ret = new int[](7);
        ret[0] = a;
        ret[1] = b;
        ret[2] = c;
        ret[3] = d;
        ret[4] = e;
        ret[5] = zero;
        ret[6] = zero2;
        return is_correct;
    }
    
    function bytes32_to_uint(bytes32 bs) internal pure returns (int256)
    {
        return int256(uint256(bs));
    }
    
    function bytesToBytes32(bytes memory b) private pure returns (bytes32) {
        bytes32 out;
        
        for (uint i = 0; i < 32; i++) {
            out |= bytes32(b[i] & 0xFF) >> (i * 8);
        }
        return out;
    }
    
    function bytes_to_bytes32(bytes[] memory b) private pure returns(bytes32[] memory){
        bytes32[] memory ret = new bytes32[](b.length);
        for (uint i = 0; i < b.length; i++) {
            ret[i] = bytesToBytes32(b[i]);
        }
        return ret;
    }
}