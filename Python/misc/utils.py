class CUtils:
    def seedir(self, path: str):
        """
            Vẽ cây thư mục
        Args:
            path (str): đường dẫn hiện tại của thư mục cần vẽ
        """
        import seedir as sd
        sd.seedir(path, style='emoji')